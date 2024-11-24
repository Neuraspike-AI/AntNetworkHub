import { createClient } from '@supabase/supabase-js'
import dotenv from 'dotenv';
dotenv.config();  // Loads the .env file

const supabaseUrl = 'https://fhuvzctwpxfznzwhpctr.supabase.co';
const supabaseAnonKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

