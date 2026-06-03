const API_URL =
  process.env.NEXT_PUBLIC_API_URL;

export async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {

  const token =
    localStorage.getItem(
      "access_token"
    );

  const response = await fetch(
    `${API_URL}${endpoint}`,
    {
      ...options,

      headers: {
        "Content-Type":
          "application/json",

        ...(token
          ? {
              Authorization:
                `Bearer ${token}`,
            }
          : {}),

        ...(options.headers || {}),
      },
    }
  );

  if (!response.ok) {

    const error =
      await response.json();

    throw new Error(
      error.detail ||
      "Something went wrong"
    );
  }

  return response.json();
}