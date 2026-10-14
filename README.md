# Job Tracker Backend: Firebase auth

Firebase handles sign-up, login, password reset and token issuing. This backend never sees a
password: it only **verifies** the Firebase ID token React sends, then uses the Firebase `uid`
as the `userId` in DynamoDB.

## One-time Firebase setup (free Spark plan is enough)

1. https://console.firebase.google.com -> create a project.
2. Build -> Authentication -> Get started -> enable **Email/Password**.
3. Project settings -> General -> add a **Web app** and copy its config object (for React).
4. Project settings -> Service accounts -> **Generate new private key**. Save the JSON as
   `serviceAccountKey.json` in this folder. **Never commit it** (it's in .gitignore).

## Backend setup

```
pip install -r requirements.txt
docker run -p 8000:8000 amazon/dynamodb-local
python scripts/setup.py
uvicorn main:app --reload --port 8080
```

Docs: http://localhost:8080/docs

## Flow

1. React signs the user up / in with the Firebase JS SDK (no backend call).
2. React gets the ID token: `await user.getIdToken()`.
3. React calls `POST /auth/sync` with `Authorization: Bearer <idToken>`. This creates the DynamoDB
   profile on first login (and returns it on later ones). Call it after every login.
4. Every other request sends the same header. Backend verifies the token and reads the `uid`.

Public: `/` only. Everything else needs a token. `/users/{user_id}/...` also requires
`user_id` == the token's uid (else 403). `GET /users/me` returns the current profile.

## React usage

```bash
npm install firebase
```

```js
// firebase.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const app = initializeApp({
  /* config object from the Firebase console */
});
export const auth = getAuth(app);
```

```js
// api.js
import { auth } from "./firebase";
const API = "http://localhost:8080";

export async function api(path, options = {}) {
  const token = await auth.currentUser.getIdToken(); // auto-refreshes when expired
  return fetch(`${API}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      ...options.headers,
    },
  });
}
```

```js
// sign up / log in
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
} from "firebase/auth";

await createUserWithEmailAndPassword(auth, email, password); // or signInWithEmailAndPassword
const res = await api("/auth/sync", {
  method: "POST",
  body: JSON.stringify({ name }),
});
const profile = await res.json();
```

## Notes

- Firebase ID tokens expire after 1 hour; the SDK refreshes them for you (`getIdToken()`).
- Verifying a token needs internet access on the backend (it fetches Google's public keys, then caches them).
  For fully offline dev, look into the Firebase Auth Emulator.
- Deleting a user here removes only the DynamoDB profile, not the Firebase account.
- Any logged-in user can `POST /jobs`. Add an admin check (Firebase custom claims) if needed.
- You can require verified emails by rejecting tokens where `email_verified` is false.
