-- SQL Script to create the messages table in Supabase
-- Run this in the Supabase SQL Editor

-- Create messages table
CREATE TABLE IF NOT EXISTS messages (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index on created_at for faster ordering
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);

-- Optional: Enable Row Level Security (RLS)
-- ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Optional: Create policy to allow all operations (for development)
-- CREATE POLICY "Allow all operations" ON messages FOR ALL USING (true);

-- Add email column to messages table
ALTER TABLE messages ADD COLUMN IF NOT EXISTS email TEXT NOT NULL DEFAULT 'anonymous@example.com';

-- Create index on email for faster queries
CREATE INDEX IF NOT EXISTS idx_messages_email ON messages(email);
