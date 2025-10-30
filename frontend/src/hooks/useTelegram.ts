import { useEffect, useMemo, useState } from "react";

type TelegramWebAppUser = {
  id: number;
  username?: string;
  first_name?: string;
  last_name?: string;
};

type TelegramWebApp = {
  initData: string;
  initDataUnsafe?: {
    user?: TelegramWebAppUser;
  };
  ready: () => void;
  expand: () => void;
  showAlert: (message: string) => void;
};

declare global {
  interface Window {
    Telegram?: {
      WebApp?: TelegramWebApp;
    };
  }
}

export function useTelegram() {
  const [initData, setInitData] = useState<string | null>(null);
  const [user, setUser] = useState<TelegramWebAppUser | null>(null);

  useEffect(() => {
    const webApp = window.Telegram?.WebApp;
    if (!webApp) {
      const fallbackId = Number(new URLSearchParams(window.location.search).get("mockUser")) || 1;
      setInitData(`user=%7B%22id%22%3A${fallbackId}%2C%22username%22%3A%22developer%22%7D&auth_date=${Date.now()}&hash=dev`);
      setUser({ id: fallbackId, username: "developer" });
      return;
    }
    webApp.ready();
    webApp.expand();
    setInitData(webApp.initData);
    if (webApp.initDataUnsafe?.user) {
      setUser(webApp.initDataUnsafe.user);
    }
  }, []);

  return useMemo(
    () => ({
      initData,
      user,
      showAlert: window.Telegram?.WebApp?.showAlert,
    }),
    [initData, user]
  );
}
