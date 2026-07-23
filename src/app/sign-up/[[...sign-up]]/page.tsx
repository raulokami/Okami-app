import { SignUp } from "@clerk/nextjs";

export default function SignUpPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center px-6 py-16">
      <SignUp />
    </main>
  );
}
