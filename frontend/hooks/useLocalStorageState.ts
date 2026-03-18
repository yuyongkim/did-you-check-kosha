"use client";

import { Dispatch, SetStateAction, useEffect, useState } from "react";

interface LocalStorageStateOptions<T> {
  serialize?: (value: T) => string;
  deserialize?: (raw: string) => T;
}

export function useLocalStorageState<T>(
  key: string,
  initialValue: T,
  options?: LocalStorageStateOptions<T>,
): [T, Dispatch<SetStateAction<T>>] {
  const serialize = options?.serialize ?? ((value: T) => JSON.stringify(value));
  const deserialize = options?.deserialize ?? ((raw: string) => JSON.parse(raw) as T);

  const [state, setState] = useState<T>(initialValue);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const raw = window.localStorage.getItem(key);
    if (!raw) {
      setState(initialValue);
      return;
    }
    try {
      setState(deserialize(raw));
    } catch {
      setState(initialValue);
    }
  }, [key, initialValue, deserialize]);

  useEffect(() => {
    if (typeof window === "undefined") return;
    try {
      window.localStorage.setItem(key, serialize(state));
    } catch {
      // noop
    }
  }, [key, serialize, state]);

  return [state, setState];
}
