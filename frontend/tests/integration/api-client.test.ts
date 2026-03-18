import { afterEach, describe, expect, it, vi } from "vitest";

import { calculateDiscipline } from "@/lib/api";

describe("calculateDiscipline", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("uses mock route in mock mode", async () => {
    const fakeResponse = { ok: true, json: async () => ({ status: "success" }) };
    const fetchSpy = vi.fn().mockResolvedValue(fakeResponse);
    vi.stubGlobal("fetch", fetchSpy);

    await calculateDiscipline("piping", { demo: true }, { apiMode: "mock", backendApiPrefix: "" });

    expect(fetchSpy).toHaveBeenCalledTimes(1);
    expect(fetchSpy.mock.calls[0][0]).toBe("/api/calculate/piping");
  });

  it("uses backend route in backend mode", async () => {
    const fakeResponse = { ok: true, json: async () => ({ status: "success" }) };
    const fetchSpy = vi.fn().mockResolvedValue(fakeResponse);
    vi.stubGlobal("fetch", fetchSpy);

    await calculateDiscipline("civil", { demo: true }, { apiMode: "backend", backendApiPrefix: "http://localhost:8000" });

    expect(fetchSpy).toHaveBeenCalledTimes(1);
    expect(fetchSpy.mock.calls[0][0]).toBe("http://localhost:8000/api/calculate/civil");
  });

  it("throws when backend mode has no prefix", async () => {
    await expect(
      calculateDiscipline("steel", { demo: true }, { apiMode: "backend", backendApiPrefix: "" }),
    ).rejects.toThrow("Backend API mode is enabled, but API prefix is empty.");
  });
});
