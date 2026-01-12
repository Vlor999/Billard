import numpy as np
from src.objects.objects import Ball


def proj_coulomb_cone(y: np.ndarray, mu: float) -> np.ndarray:
    yN, yT = y

    # Case 1: separation
    if yN <= 0:
        return np.zeros(2)

    # Case 2: sticking
    if abs(yT) <= mu * yN:
        return y

    # Case 3: sliding
    rN = (yN + mu * abs(yT)) / (1 + mu**2)
    rT = mu * rN * np.sign(yT)
    return np.array([rN, rT])


def proj_disk(x: np.ndarray, R: float) -> np.ndarray:
    norm = np.linalg.norm(x)
    if norm <= R:
        return x
    return (R / norm) * x


class Contact:
    def __init__(self, mu: float, e: float):
        self.mu = mu
        self.e = e
        self.r = np.zeros(2)  # [rN, rT]

    def solve_local(self) -> np.ndarray:
        raise NotImplementedError

    def apply_delta_impulse(self, dr):
        raise NotImplementedError


class BallWallContact(Contact):
    def __init__(self, ball: Ball, n, mu: float, e: float) -> None:
        super().__init__(mu, e)
        self.ball = ball
        self.n = n / np.linalg.norm(n)
        self.t = np.array([-self.n[1], self.n[0]])

    def solve_local(self) -> np.ndarray:
        b = self.ball

        # vitesse au point de contact
        v_c = b.v - b.omega * b.R * self.t

        uN = np.dot(self.n, v_c)
        uT = np.dot(self.t, v_c)

        if uN >= 0:
            return np.zeros(2)

        u_free = np.array([(1 + self.e) * uN, uT])

        W = np.diag([1.0 / b.m, 1.0 / b.m + b.R**2 / b.I])

        rho = np.linalg.inv(W)

        r_trial = self.r - rho @ (u_free + W @ self.r)
        r_new = proj_coulomb_cone(r_trial, self.mu)

        dr = r_new - self.r
        self.r = r_new
        return dr

    def apply_delta_impulse(self, dr: np.ndarray) -> None:
        try:
            b = self.ball
            impulse = dr[0] * self.n + dr[1] * self.t

            b.v += impulse / b.m
            b.omega += (-b.R * dr[1]) / b.I
        except:
            print("b.I=", b.I, ", dr=", dr, ", b.R=", b.R)
            raise Exception("Issue 1")


class BallBallContact(Contact):
    def __init__(self, A: Ball, B: Ball, mu: float, e: float) -> None:
        super().__init__(mu, e)
        self.A = A
        self.B = B

        d = B.q - A.q
        dist = np.linalg.norm(d)
        self.n = d / dist
        self.t = np.array([-self.n[1], self.n[0]])

    def solve_local(self) -> np.ndarray:
        A, B = self.A, self.B

        # Relative velocity at contact
        vA_c = A.v + A.omega * A.R * self.t
        vB_c = B.v - B.omega * B.R * self.t
        u = vB_c - vA_c

        uN = np.dot(self.n, u)
        uT = np.dot(self.t, u)

        if uN >= 0:
            return np.zeros(2)

        # Restitution
        u_free = np.array([(1 + self.e) * uN, uT])

        W = np.diag(
            [1 / A.m + 1 / B.m, 1 / A.m + 1 / B.m + A.R**2 / A.I + B.R**2 / B.I]
        )

        rho = np.linalg.inv(W)
        r_trial = self.r - rho @ (u_free + W @ self.r)

        r_new = proj_coulomb_cone(r_trial, self.mu)
        dr = r_new - self.r
        self.r = r_new

        return dr

    def apply_delta_impulse(self, dr: np.ndarray) -> None:
        impulse = dr[0] * self.n + dr[1] * self.t

        self.A.v -= impulse / self.A.m
        self.B.v += impulse / self.B.m

        self.A.omega -= self.A.R * dr[1] / self.A.I
        self.B.omega -= self.B.R * dr[1] / self.B.I


def solve_contacts_NSGS(
    contacts: list[Contact], max_iter: int = 20000, min_err: float = 1e-5
) -> None:
    it = 0
    err = float("inf")
    if len(contacts) == 0:
        return
    while it <= max_iter and err >= min_err:
        for c in contacts:
            dr = c.solve_local()
            c.apply_delta_impulse(dr)
            err = min(np.linalg.norm(dr), err)
        it += 1


def ball_ball_kinematics(
    A: Ball, B: Ball
) -> tuple[float, np.ndarray, np.ndarray, np.ndarray]:
    d = B.q - A.q
    dist = np.linalg.norm(d)
    n = d / dist
    t = np.array([-n[1], n[0]])

    # Relative velocity at contact
    vA_c = A.v + A.omega * A.R * t
    vB_c = B.v - B.omega * B.R * t
    u = vB_c - vA_c

    uN = np.dot(n, u)
    uT = np.dot(t, u)

    return float(dist - (A.R + B.R)), n, t, np.array([uN, uT])


def detect_wall_contacts(
    ball: Ball, box: list[int], mu: float, e: float
) -> list[Contact]:
    contacts = []

    x, y = ball.q
    R = ball.R
    xmin, xmax, ymin, ymax = box

    if x - R <= xmin:
        contacts.append(BallWallContact(ball, np.array([1, 0]), mu, e))
    if x + R >= xmax:
        contacts.append(BallWallContact(ball, np.array([-1, 0]), mu, e))
    if y - R <= ymin:
        contacts.append(BallWallContact(ball, np.array([0, 1]), mu, e))
    if y + R >= ymax:
        contacts.append(BallWallContact(ball, np.array([0, -1]), mu, e))

    return contacts


def detect_ball_ball_contacts(balls, mu, e):
    contacts = []
    nballs = len(balls)

    for i in range(nballs):
        for j in range(i + 1, nballs):
            A, B = balls[i], balls[j]
            d = B.q - A.q
            dist = np.linalg.norm(d)

            if dist <= A.R + B.R:
                contacts.append(BallBallContact(A, B, mu, e))

    return contacts


def detect_contacts(balls: list[Ball], box, mu: float, e: float) -> list[Contact]:
    contacts: list[Contact] = []
    for b in balls:
        contacts += detect_wall_contacts(b, box, mu, e)
    contacts += detect_ball_ball_contacts(balls, mu, e)
    return contacts


def project_positions(balls: list[Ball], box) -> None:
    xmin, xmax, ymin, ymax = box
    for b in balls:
        b.q[0] = np.clip(b.q[0], xmin + b.R, xmax - b.R)
        b.q[1] = np.clip(b.q[1], ymin + b.R, ymax - b.R)


def apply_floor_friction(ball: Ball, mu: float, dt: float, err: float = 1e-6) -> None:
    g = 9.81
    normal_impulse = ball.m * g * dt
    norm_v = np.linalg.norm(ball.v)

    if norm_v > err:
        friction_impulse_mag = mu * normal_impulse
        momentum = ball.m * norm_v
        impulse_mag = min(friction_impulse_mag, momentum)
        v_dir = ball.v / norm_v
        ball.v -= (impulse_mag * v_dir) / ball.m
    else:
        ball.v = np.zeros_like(ball.v)

    if abs(ball.omega) > err:
        spin_impulse_mag = mu * normal_impulse * ball.R
        angular_momentum = ball.I * abs(ball.omega)
        delta_omega = min(spin_impulse_mag, angular_momentum)
        sign = np.sign(ball.omega)
        ball.omega -= (delta_omega * sign) / ball.I
    else:
        ball.omega = 0.0


def step_system(balls: list[Ball], box, mu: float, e: float, dt: float) -> None:
    # --- wall + ball contacts ---
    contacts = detect_contacts(balls, box, mu, e)
    solve_contacts_NSGS(contacts)

    # --- floor friction (2.5D) ---
    for b in balls:
        apply_floor_friction(b, mu, dt)

    # --- integrate ---
    for b in balls:
        b.q += dt * b.v
        b.theta += dt * b.omega

    project_positions(balls, box)
