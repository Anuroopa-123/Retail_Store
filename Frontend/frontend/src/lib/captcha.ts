export const generateCaptcha =
(): string => {

  const chars =
    "ABCDEFGHJKLMNPQRSTUVWXYZ123456789";

  let text = "";

  for (
    let i = 0;
    i < 6;
    i++
  ) {

    text += chars[
      Math.floor(
        Math.random() *
        chars.length
      )
    ];
  }

  return text;
};