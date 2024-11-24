import { supabase } from './supabase.js';
import { v4 as uuidv4 } from 'uuid';
// Import the HTTP module

(async () => {
    const newId = uuidv4();
    const currentTimestamp = new Date().toISOString();
    const { data, error } = await supabase
      .from('nodes')
      .insert([
        { id: newId, last_connection: currentTimestamp },
      ]);
  
    if (error) {
      console.error('Error inserting data:', error);
    } else {
      console.log('Data inserted:', data);
    }
  })();

import express from 'express';
import bodyParser from 'body-parser'; 

// Initialize the express app
const app = express();
const port = 3000;

// Use body-parser middleware to parse incoming JSON data
app.use(bodyParser.json());  // or app.use(express.json()) if you are using Express 4.16+

// Define a POST route
app.post('/log_user', (req, res) => {
  // Access POST data from the body
  const data = req.body;

  // Log the data to the console
  console.log('Received data:', data);

  // Send a response back
  res.json({
    message: 'Data received successfully!',
    data: data
  });
});


// Start the server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
