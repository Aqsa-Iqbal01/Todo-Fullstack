---
name: nextjs
description: Comprehensive Next.js development assistance including project setup, routing, API routes, data fetching, authentication, styling, and deployment. Use when Claude needs to work with Next.js for: (1) Creating new Next.js projects, (2) Implementing page routing and navigation, (3) Building API routes, (4) Data fetching strategies (getServerSideProps, getStaticProps, getStaticPaths), (5) Adding authentication, (6) Styling with Tailwind CSS or other solutions, (7) Handling forms and state, or (8) Deployment configuration.
---

# Nextjs

## Overview

Next.js is a React framework that enables functionality such as hybrid static & server rendering, TypeScript support, smart bundling, route pre-fetching, and more. This skill provides comprehensive assistance for developing Next.js applications including project structure, routing, data fetching, API routes, styling, authentication, and deployment.

## Quick Start Guide

### Creating a Basic Next.js Application

```bash
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
cd my-app
npm run dev
```

### Basic Page Structure

```tsx
// src/app/page.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Home',
}

export default function HomePage() {
  return (
    <main>
      <h1>Hello, Next.js!</h1>
    </main>
  )
}
```

## Core Capabilities

### 1. Project Structure

Create a standard Next.js project structure:

```
my-nextjs-app/
├── src/
│   ├── app/               # App Router (Next.js 13+)
│   │   ├── layout.tsx     # Root layout
│   │   ├── page.tsx       # Home page
│   │   ├── globals.css    # Global styles
│   │   └── ...            # Other pages and nested routes
│   ├── components/        # Reusable React components
│   ├── lib/               # Utility functions and services
│   ├── hooks/             # Custom React hooks
│   └── types/             # TypeScript type definitions
├── public/                # Static assets
├── next.config.js         # Next.js configuration
├── tailwind.config.js     # Tailwind CSS configuration
├── tsconfig.json          # TypeScript configuration
└── package.json
```

### 2. Routing

#### Page-based Routing (App Router)

```tsx
// src/app/dashboard/page.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Dashboard',
}

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome to your dashboard!</p>
    </div>
  )
}
```

#### Dynamic Routes

```tsx
// src/app/users/[id]/page.tsx
import { notFound } from 'next/navigation'

interface UserPageProps {
  params: {
    id: string
  }
}

export default async function UserPage({ params }: UserPageProps) {
  const user = await getUser(params.id)

  if (!user) {
    notFound()
  }

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  )
}
```

#### Route Groups

```tsx
// src/app/(auth)/login/page.tsx
// Routes in (auth) group won't have the auth layout wrapper
export default function LoginPage() {
  return <div>Login Form</div>
}
```

### 3. Data Fetching

#### Server-Side Rendering (SSR)

```tsx
// src/app/users/page.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Users',
}

interface UsersPageProps {
  searchParams: { [key: string]: string | string[] | undefined }
}

export default async function UsersPage({ searchParams }: UsersPageProps) {
  const page = searchParams.page ? parseInt(searchParams.page as string) : 1
  const users = await getUsers({ page })

  return (
    <div>
      <h1>Users</h1>
      <ul>
        {users.map(user => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  )
}

async function getUsers({ page }: { page: number }) {
  // Implementation here
  return []
}
```

#### Static Site Generation (SSG)

```tsx
// src/app/posts/[slug]/page.tsx
import { notFound } from 'next/navigation'

interface PostPageProps {
  params: {
    slug: string
  }
}

export async function generateStaticParams() {
  const posts = await getAllPosts()
  return posts.map((post) => ({
    slug: post.slug,
  }))
}

export async function generateMetadata({ params }: PostPageProps) {
  const post = await getPost(params.slug)

  if (!post) {
    return {}
  }

  return {
    title: post.title,
  }
}

export default async function PostPage({ params }: PostPageProps) {
  const post = await getPost(params.slug)

  if (!post) {
    notFound()
  }

  return (
    <article>
      <h1>{post.title}</h1>
      <div>{post.content}</div>
    </article>
  )
}
```

### 4. API Routes

#### Basic API Route

```ts
// src/app/api/users/route.ts
import { NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const page = searchParams.get('page')

  const users = await getUsers({ page: page || '1' })

  return Response.json({ users })
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const user = await createUser(body)

  return Response.json({ user }, { status: 201 })
}
```

#### Authentication API Route

```ts
// src/app/api/auth/login/route.ts
import { NextRequest } from 'next/server'
import { cookies } from 'next/headers'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { email, password } = body

    // Validate credentials
    const user = await validateUser(email, password)

    if (!user) {
      return Response.json({ error: 'Invalid credentials' }, { status: 401 })
    }

    // Set session cookie
    cookies().set('session', user.sessionToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      maxAge: 60 * 60 * 24 * 7, // 1 week
      path: '/',
    })

    return Response.json({ user })
  } catch (error) {
    return Response.json({ error: 'Internal server error' }, { status: 500 })
  }
}
```

### 5. Client Components and Server Components

#### Server Component (default in App Router)

```tsx
// Server components can directly access data
export default async function UserList() {
  const users = await getUsers()

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

#### Client Component

```tsx
'use client'

import { useState, useEffect } from 'react'

export default function ClientComponent() {
  const [data, setData] = useState(null)

  useEffect(() => {
    // Client-side data fetching
    fetch('/api/data')
      .then(res => res.json())
      .then(setData)
  }, [])

  return <div>{data ? JSON.stringify(data) : 'Loading...'}</div>
}
```

### 6. Styling

#### Global Styles

```css
/* src/app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 47.4% 11.2%;
  }
}

body {
  @apply bg-background text-foreground;
}
```

#### Component Styling with Tailwind

```tsx
// src/components/Button.tsx
import { ReactNode } from 'react'

interface ButtonProps {
  children: ReactNode
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  onClick?: () => void
}

export default function Button({
  children,
  variant = 'primary',
  size = 'md',
  onClick
}: ButtonProps) {
  const baseClasses = 'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2'

  const variantClasses = {
    primary: 'bg-primary text-primary-foreground hover:bg-primary/90',
    secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
    ghost: 'hover:bg-accent hover:text-accent-foreground',
  }

  const sizeClasses = {
    sm: 'h-9 px-3 rounded-md text-sm',
    md: 'h-10 px-4 py-2',
    lg: 'h-11 px-8 rounded-md text-lg',
  }

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]}`}
      onClick={onClick}
    >
      {children}
    </button>
  )
}
```

### 7. Forms and State Management

#### Form with Server Action

```tsx
// src/app/contact/page.tsx
'use server'

import { z } from 'zod'
import { redirect } from 'next/navigation'

const ContactFormSchema = z.object({
  name: z.string().min(1, { message: 'Name is required' }),
  email: z.string().email({ message: 'Invalid email address' }),
  message: z.string().min(10, { message: 'Message must be at least 10 characters' }),
})

export default function ContactPage() {
  async function createContact(prevState: any, formData: FormData) {
    try {
      const validatedFields = ContactFormSchema.parse({
        name: formData.get('name'),
        email: formData.get('email'),
        message: formData.get('message'),
      })

      // Process the form data
      await saveContact(validatedFields)

      // Redirect after successful submission
      redirect('/contact/success')
    } catch (error) {
      if (error instanceof z.ZodError) {
        return {
          errors: error.flatten().fieldErrors,
          message: 'Missing Fields. Failed to Create Invoice.',
        }
      }

      return {
        message: 'Database Error: Failed to Create Invoice.',
      }
    }
  }

  return (
    <form action={createContact}>
      <div>
        <label htmlFor="name">Name</label>
        <input id="name" name="name" type="text" required />
      </div>
      <div>
        <label htmlFor="email">Email</label>
        <input id="email" name="email" type="email" required />
      </div>
      <div>
        <label htmlFor="message">Message</label>
        <textarea id="message" name="message" required />
      </div>
      <button type="submit">Send Message</button>
    </form>
  )
}
```

### 8. Authentication

#### Protected Route Middleware

```ts
// middleware.ts
import { NextRequest, NextResponse } from 'next/server'
import { getToken } from 'next-auth/jwt'

export async function middleware(request: NextRequest) {
  // Define protected routes
  const protectedPaths = ['/dashboard', '/admin']
  const isProtectedPath = protectedPaths.some(path =>
    request.nextUrl.pathname.startsWith(path)
  )

  if (isProtectedPath) {
    const token = await getToken({
      req: request,
      secret: process.env.NEXTAUTH_SECRET
    })

    if (!token) {
      const url = request.nextUrl.clone()
      url.pathname = '/login'
      url.search = `callbackUrl=${request.nextUrl.pathname}`
      return NextResponse.redirect(url)
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*', '/login', '/register']
}
```

### 9. Environment Variables

#### Environment Configuration

```ts
// src/lib/env.ts
import { z } from 'zod'

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  DATABASE_URL: z.string().url(),
  NEXTAUTH_URL: z.string().url(),
  NEXTAUTH_SECRET: z.string(),
  GITHUB_ID: z.string(),
  GITHUB_SECRET: z.string(),
})

export const env = envSchema.parse(process.env)
```

### 10. Deployment

#### Production Build Configuration

```js
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverActions: true,
  },
  images: {
    domains: ['avatars.githubusercontent.com'],
  },
  async redirects() {
    return [
      {
        source: '/docs',
        destination: '/docs/introduction',
        permanent: true,
      },
    ]
  },
}

module.exports = nextConfig
```

## Resources

This skill includes example resource directories that demonstrate how to organize different types of bundled resources:

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Appropriate for:** Scripts for project generation, build automation, testing utilities, or any executable code that performs automation, data processing, or specific operations.

### references/
Documentation and reference material intended to be loaded into context to inform Claude's process and thinking.

**Appropriate for:** Next.js documentation, API reference documentation, component libraries, comprehensive guides, or any detailed information that Claude should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Claude produces.

**Appropriate for:** Project templates, boilerplate code, configuration files, or any files meant to be copied or used in the final output.

---

**Any unneeded directories can be deleted.** Not every skill requires all three types of resources.