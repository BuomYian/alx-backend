// Importing necessary modules
import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const app = express();
const port = 1245;

// Define the list of products
const listProducts = [
  {
    itemId: 1,
    itemName: 'Suitcase 250',
    price: 50,
    initialAvailableQuantity: 4,
  },
  {
    itemId: 2,
    itemName: 'Suitcase 450',
    price: 100,
    initialAvailableQuantity: 10,
  },
  {
    itemId: 3,
    itemName: 'Suitcase 650',
    price: 350,
    initialAvailableQuantity: 2,
  },
  {
    itemId: 4,
    itemName: 'Suitcase 1050',
    price: 550,
    initialAvailableQuantity: 5,
  },
];

// Create a Redis client
const redisClient = redis.createClient();

// Promisify Redis methods
const redisGet = promisify(redisClient.get).bind(redisClient);
const redisSet = promisify(redisClient.set).bind(redisClient);

// Middleware to handle JSON body
app.use(express.json());

// Get the list of all products
app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

// Get product details by itemId
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = listProducts.find((item) => item.itemId === itemId);

  if (!product) {
    res.json({ status: 'Product not found' });
  } else {
    const currentQuantity = await getCurrentReservedStockById(itemId);
    res.json({ ...product, currentQuantity });
  }
});

// Reserve a product by itemId
app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = listProducts.find((item) => item.itemId === itemId);

  if (!product) {
    res.json({ status: 'Product not found' });
  } else {
    const currentQuantity = await getCurrentReservedStockById(itemId);

    if (currentQuantity <= 0) {
      res.json({ status: 'Not enough stock available', itemId });
    } else {
      await reserveStockById(itemId, currentQuantity - 1);
      res.json({ status: 'Reservation confirmed', itemId });
    }
  }
});

// Reserve stock by itemId
async function reserveStockById(itemId, stock) {
  await redisSet(`item.${itemId}`, stock);
}

// Get current reserved stock by itemId
async function getCurrentReservedStockById(itemId) {
  const reservedStock = await redisGet(`item.${itemId}`);
  return parseInt(reservedStock, 10) || 0;
}

// Start the server
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});
