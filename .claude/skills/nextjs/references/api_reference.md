# Next.js Reference Guide

## API Documentation

This document provides comprehensive reference material for Next.js development.

## Routing

### App Router (Next.js 13+)

The App Router is built on the concept of file-based routing using the `app` directory.

#### Basic Route

```tsx
// src/app/page.tsx
export default function Page() {
  return <h1>Hello, Next.js!</h1>
}
```

#### Dynamic Routes

```tsx
// src/app/blog/[slug]/page.tsx
interface BlogPostPageProps {
  params: {
    slug: string
  }
}

export default function BlogPostPage({ params }: BlogPostPageProps) {
  return <h1>Blog post: {params.slug}</h1>
}
```

#### Catch-all Routes

```tsx
// src/app/docs/[...slug]/page.tsx
interface DocsPageProps {
  params: {
    slug: string[]
  }
}

export default function DocsPage({ params }: DocsPageProps) {
  return <h1>Docs: {params.slug.join('/')}</h1>
}
```

#### Optional Catch-all Routes

```tsx
// src/app/shop/[[...slug]]/page.tsx
interface ShopPageProps {
  params: {
    slug?: string[]
  }
}

export default function ShopPage({ params }: ShopPageProps) {
  return <h1>Shop: {params.slug?.join('/') || 'home'}</h1>
}
```

### Route Groups

```tsx
// src/app/(marketing)/layout.tsx
export default function MarketingLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <section className="marketing">
      {children}
    </section>
  )
}
```

## Data Fetching

### Server-Side Rendering (SSR)

```tsx
// src/app/users/page.tsx
export default async function UsersPage() {
  const users = await getUsers()

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}

async function getUsers() {
  const res = await fetch('https://api.example.com/users')
  return res.json()
}
```

### Static Site Generation (SSG)

```tsx
// src/app/posts/[slug]/page.tsx
interface PostPageProps {
  params: {
    slug: string
  }
}

export async function generateStaticParams() {
  const posts = await getPosts()
  return posts.map((post) => ({
    slug: post.slug,
  }))
}

export default async function PostPage({ params }: PostPageProps) {
  const post = await getPost(params.slug)

  return (
    <article>
      <h1>{post.title}</h1>
      <div>{post.content}</div>
    </article>
  )
}
```

### Streaming

```tsx
// src/app/dashboard/page.tsx
import { Suspense } from 'react'
import { Card } from '@/components/Card'
import { Metric } from '@/components/Metric'

export default function Dashboard() {
  return (
    <div>
      <header>
        <h1>Dashboard</h1>
      </header>
      <Suspense fallback={<Metric.Skeleton />}>
        <Metric />
      </Suspense>
      <Suspense fallback={<Card.Skeleton />}>
        <Card />
      </Suspense>
    </div>
  )
}
```

## API Routes

### Basic API Route

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

### API Route with Dynamic Segments

```ts
// src/app/api/users/[id]/route.ts
import { NextRequest } from 'next/server'

interface RouteProps {
  params: {
    id: string
  }
}

export async function GET(request: NextRequest, { params }: RouteProps) {
  const user = await getUser(params.id)

  if (!user) {
    return Response.json({ error: 'User not found' }, { status: 404 })
  }

  return Response.json({ user })
}

export async function PUT(request: NextRequest, { params }: RouteProps) {
  const body = await request.json()
  const updatedUser = await updateUser(params.id, body)

  return Response.json({ user: updatedUser })
}

export async function DELETE(request: NextRequest, { params }: RouteProps) {
  await deleteUser(params.id)

  return new Response(null, { status: 204 })
}
```

## Client Components

### Using 'use client' Directive

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

### Client Component with Server Action

```tsx
'use client'

import { useFormState, useFormStatus } from 'react-dom'
import { submitForm } from '@/actions/form'

function SubmitButton() {
  const { pending } = useFormStatus()

  return (
    <button type="submit" aria-disabled={pending}>
      {pending ? 'Submitting...' : 'Submit'}
    </button>
  )
}

export default function ContactForm() {
  const [state, formAction] = useFormState(submitForm, null)

  return (
    <form action={formAction}>
      <label htmlFor="name">Name</label>
      <input type="text" id="name" name="name" required />

      <label htmlFor="email">Email</label>
      <input type="email" id="email" name="email" required />

      <SubmitButton />
      {state?.message && <p>{state.message}</p>}
    </form>
  )
}
```

## Server Actions

### Basic Server Action

```ts
// src/actions/form.ts
'use server'

import { z } from 'zod'

const FormSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
})

export async function submitForm(prevState: any, formData: FormData) {
  try {
    const validatedFields = FormSchema.parse({
      name: formData.get('name'),
      email: formData.get('email'),
    })

    // Process the validated data
    await saveToDatabase(validatedFields)

    return { message: 'Form submitted successfully!' }
  } catch (error) {
    if (error instanceof z.ZodError) {
      return { message: 'Invalid form data' }
    }

    return { message: 'An error occurred' }
  }
}
```

## Styling

### Global Styles

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

### Component Styles with Tailwind

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

## Metadata

### Static Metadata

```tsx
// src/app/page.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Home',
  description: 'Welcome to Next.js',
}

export default function HomePage() {
  return <h1>Home Page</h1>
}
```

### Dynamic Metadata

```tsx
// src/app/blog/[slug]/page.tsx
import { Metadata } from 'next'

interface BlogPostPageProps {
  params: {
    slug: string
  }
}

export async function generateMetadata({ params }: BlogPostPageProps): Promise<Metadata> {
  const post = await getPost(params.slug)

  return {
    title: post.title,
    description: post.excerpt,
  }
}

export default function BlogPostPage({ params }: BlogPostPageProps) {
  // Component implementation
}
```

## Image Optimization

### Next.js Image Component

```tsx
import Image from 'next/image'

export default function MyImage() {
  return (
    <Image
      src="/me.png"
      alt="Picture of the author"
      width={500}
      height={500}
      // Optional: blur-up placeholder
      placeholder="blur"
      blurDataURL="/me-blur.png"
    />
  )
}
```

## Link Component

### Client-side Navigation

```tsx
import Link from 'next/link'

export default function Navigation() {
  return (
    <nav>
      <Link href="/">Home</Link>
      <Link href="/about">About</Link>
      <Link href="/dashboard">Dashboard</Link>
    </nav>
  )
}
```

### Prefetching

```tsx
// Prefetch by default (in the viewport)
<Link href="/dashboard">Dashboard</Link>

// Disable prefetching
<Link href="/dashboard" prefetch={false}>Dashboard</Link>
```

## Environment Variables

### Environment Configuration

```ts
// src/lib/env.ts
import { z } from 'zod'

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  DATABASE_URL: z.string().url(),
  NEXTAUTH_URL: z.string().url(),
  NEXTAUTH_SECRET: z.string(),
})

export const env = envSchema.parse(process.env)
```

### Using Environment Variables

```ts
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    customKey: process.env.CUSTOM_ENV,
  },
  experimental: {
    serverActions: true,
  },
}

module.exports = nextConfig
```

## Middleware

### Basic Middleware

```ts
// middleware.ts
import { NextRequest, NextResponse } from 'next/server'

export function middleware(request: NextRequest) {
  // Example: Redirect unauthenticated users from dashboard
  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    const token = request.cookies.get('token')

    if (!token) {
      return NextResponse.redirect(new URL('/login', request.url))
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*']
}
```

## Error Handling

### Global Error Component

```tsx
// src/app/error.tsx
'use client'

import { useEffect } from 'react'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error(error)
  }, [error])

  return (
    <div>
      <h2>Something went wrong!</h2>
      <button
        onClick={
          () => reset()
        }
      >
        Try again
      </button>
    </div>
  )
}
```

### Not Found Component

```tsx
// src/app/not-found.tsx
export default function NotFound() {
  return (
    <div>
      <h2>Not Found</h2>
      <p>Could not find requested resource</p>
    </div>
  )
}
```

## Loading UI

### Loading Component

```tsx
// src/app/dashboard/loading.tsx
export default function DashboardLoading() {
  return (
    <div>
      <p>Loading dashboard...</p>
    </div>
  )
}
```

### Suspense-based Loading

```tsx
// src/app/dashboard/page.tsx
import { Suspense } from 'react'
import DashboardContent from './dashboard-content'

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<p>Loading feed...</p>}>
        <DashboardContent />
      </Suspense>
    </div>
  )
}
```

## Testing

### Jest Configuration

```js
// jest.config.js
const nextJest = require('next/jest')

const createJestConfig = nextJest({
  dir: './',
})

const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jest-environment-jsdom',
}

module.exports = createJestConfig(customJestConfig)
```

### Example Test

```tsx
// src/components/Button.test.tsx
import { render, screen } from '@testing-library/react'
import Button from './Button'

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })
})
```