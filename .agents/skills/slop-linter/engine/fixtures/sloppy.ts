interface User { id: string; email: string; active: boolean }
export type UserId = string;

export function sloppy(users: User[]): string[] {
  return users.filter((u) => u.active).map((u) => u.email);
}
export function widen(input: object): User {
  const user = input as object as User;
  return user;
}
export function runtimeCheck(input: unknown): string {
  if (typeof input === "string") { return input; }
  return "";
}
export function unsafeDict(value: string): UserId {
  const userId = value as UserId;
  return userId;
}
