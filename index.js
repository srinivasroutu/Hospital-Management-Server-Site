const express = require('express');
const cors = require('cors');
require('dotenv').config();
const { MongoClient, ServerApiVersion } = require('mongodb');

const app = express();
const port = process.env.PORT || 5000;
app.use(cors());
app.use(express.json());
const uri = `mongodb+srv://${process.env.DB_USER}:${process.env.DB_PASS}@cluster0.twtll.mongodb.net/myFirstDatabase?retryWrites=true&w=majority`;
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true, serverApi: ServerApiVersion.v1 });
async function run() {
    try {
        await client.connect();
        const database = client.db("hospital");
        constdoctorsCollection = database.collection("doctors");
   
        // get api for all doctor
        app.get('/doctors', async (req, res) => {
            const cursor =doctorsCollection.find({});
            const doctors = await cursor.toArray();
            res.send(doctors);
        });
        app.post('/doctors', async (req, res) => {
            const doctor = req.body;
            const resultP = awaitdoctorsCollection.insertOne(doctor);
            console.log(resultP);
            res.json(resultP)
        });
       
    } finally {
        // await client.close();
    }
}

app.get('/', (req, res) => {
  res.send('Hello From Doctor!')
})

app.listen(port, () => {
  console.log(`Doctors App listening  ${port}`)
})