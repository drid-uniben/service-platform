import bcrypt from "bcryptjs";
import type { Request, Response } from "express";
import { signAccessToken } from "../utils/token.js";

type StoredUser = {
  id: string;
  email: string;
  passwordHash: string;
  name?: string;
};

const usersByEmail = new Map<string, StoredUser>();

function sanitizeUser(user: StoredUser) {
  return {
    id: user.id,
    email: user.email,
    name: user.name ?? null,
  };
}

export async function register(req: Request, res: Response): Promise<void> {
  const { email, password, name } = req.body as {
    email?: string;
    password?: string;
    name?: string;
  };

  if (!email || !password) {
    res.status(400).json({ message: "email and password are required" });
    return;
  }

  const normalizedEmail = email.trim().toLowerCase();

  if (usersByEmail.has(normalizedEmail)) {
    res.status(409).json({ message: "User already exists" });
    return;
  }

  const passwordHash = await bcrypt.hash(password, 10);
  const user: StoredUser = {
    id: crypto.randomUUID(),
    email: normalizedEmail,
    passwordHash,
    name: name?.trim(),
  };

  usersByEmail.set(normalizedEmail, user);

  const token = signAccessToken({ sub: user.id, email: user.email });

  res.status(201).json({
    message: "User registered",
    user: sanitizeUser(user),
    accessToken: token,
  });
}

export async function login(req: Request, res: Response): Promise<void> {
  const { email, password } = req.body as {
    email?: string;
    password?: string;
  };

  if (!email || !password) {
    res.status(400).json({ message: "email and password are required" });
    return;
  }

  const normalizedEmail = email.trim().toLowerCase();
  const user = usersByEmail.get(normalizedEmail);

  if (!user) {
    res.status(401).json({ message: "Invalid credentials" });
    return;
  }

  const passwordMatch = await bcrypt.compare(password, user.passwordHash);
  if (!passwordMatch) {
    res.status(401).json({ message: "Invalid credentials" });
    return;
  }

  const token = signAccessToken({ sub: user.id, email: user.email });

  res.status(200).json({
    message: "Login successful",
    user: sanitizeUser(user),
    accessToken: token,
  });
}

export function getMe(req: Request, res: Response): void {
  if (!req.user?.email) {
    res.status(401).json({ message: "Unauthorized" });
    return;
  }

  const user = usersByEmail.get(req.user.email.toLowerCase());

  if (!user) {
    res.status(404).json({ message: "User not found" });
    return;
  }

  res.status(200).json({ user: sanitizeUser(user) });
}
