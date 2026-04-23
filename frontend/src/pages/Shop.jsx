import { useState, useEffect } from "react";
import API from "../api";

function Shop() {
  const [products, setProducts] = useState([]);
  const [search, setSearch] = useState("");
  const [form, setForm] = useState({
    name: "",
    description: "",
    price: "",
    stock: "",
  });
  const token = localStorage.getItem("token");

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async (searchTerm = "") => {
    try {
      const res = await API.get(`/products/?search=${searchTerm}`);
      setProducts(res.data);
    } catch (err) {
      console.error("Error fetching products", err);
    }
  };

  const handleSearch = (e) => {
    setSearch(e.target.value);
    fetchProducts(e.target.value);
  };

  const createProduct = async (e) => {
    e.preventDefault();
    try {
      await API.post("/products/", {
        ...form,
        price: parseFloat(form.price),
        stock: parseInt(form.stock),
      });
      setForm({ name: "", description: "", price: "", stock: "" });
      fetchProducts();
    } catch (err) {
      console.error("Error creating product", err);
    }
  };

  const deleteProduct = async (id) => {
    await API.delete(`/products/${id}`);
    fetchProducts();
  };

  return (
    <div className="mt-8">
      <h2 className="text-2xl font-bold mb-6">Shop 🛍️</h2>

      {/* Search */}
      <input
        type="text"
        placeholder="🔍 Search products..."
        value={search}
        onChange={handleSearch}
        className="border p-3 rounded w-full mb-6"
      />

      {/* Add Product Form (only if logged in) */}
      {token && (
        <form
          onSubmit={createProduct}
          className="bg-white p-6 rounded shadow mb-6 grid grid-cols-2 gap-3"
        >
          <input
            type="text"
            placeholder="Product name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            className="border p-3 rounded"
            required
          />
          <input
            type="text"
            placeholder="Description"
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
            className="border p-3 rounded"
          />
          <input
            type="number"
            placeholder="Price"
            value={form.price}
            onChange={(e) => setForm({ ...form, price: e.target.value })}
            className="border p-3 rounded"
            required
          />
          <input
            type="number"
            placeholder="Stock"
            value={form.stock}
            onChange={(e) => setForm({ ...form, stock: e.target.value })}
            className="border p-3 rounded"
            required
          />
          <button
            type="submit"
            className="col-span-2 bg-blue-600 text-white p-3 rounded hover:bg-blue-700"
          >
            Add Product
          </button>
        </form>
      )}

      {/* Products Grid */}
      <div className="grid grid-cols-2 gap-4">
        {products.length === 0 && (
          <p className="text-gray-500 col-span-2 text-center">
            No products found!
          </p>
        )}
        {products.map((product) => (
          <div key={product.id} className="bg-white p-6 rounded shadow">
            <div className="flex justify-between items-start">
              <h3 className="text-lg font-bold">{product.name}</h3>
              {token && (
                <button
                  onClick={() => deleteProduct(product.id)}
                  className="text-red-500 hover:text-red-700"
                >
                  ✕
                </button>
              )}
            </div>
            <p className="text-gray-500 text-sm mb-3">{product.description}</p>
            <div className="flex justify-between items-center">
              <span className="text-blue-600 font-bold text-xl">
                ₹{product.price}
              </span>
              <span className="text-gray-500 text-sm">
                Stock: {product.stock}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Shop;