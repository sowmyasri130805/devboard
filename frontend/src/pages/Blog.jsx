import { useState, useEffect } from "react";
import API from "../api";

function Blog() {
  const [posts, setPosts] = useState([]);
  const [form, setForm] = useState({ title: "", content: "" });
  const token = localStorage.getItem("token");

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const res = await API.get("/posts/");
      setPosts(res.data);
    } catch (err) {
      console.error("Error fetching posts", err);
    }
  };

  const createPost = async (e) => {
    e.preventDefault();
    try {
      await API.post("/posts/", { ...form, published: true });
      setForm({ title: "", content: "" });
      fetchPosts();
    } catch (err) {
      console.error("Error creating post", err);
    }
  };

  const deletePost = async (id) => {
    await API.delete(`/posts/${id}`);
    fetchPosts();
  };

  return (
    <div className="mt-8">
      <h2 className="text-2xl font-bold mb-6">Blog Posts 📰</h2>

      {/* Create Post Form (only if logged in) */}
      {token && (
        <form
          onSubmit={createPost}
          className="bg-white p-6 rounded shadow mb-6 flex flex-col gap-3"
        >
          <input
            type="text"
            placeholder="Post title"
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            className="border p-3 rounded"
            required
          />
          <textarea
            placeholder="Post content"
            value={form.content}
            onChange={(e) => setForm({ ...form, content: e.target.value })}
            className="border p-3 rounded h-32"
            required
          />
          <button
            type="submit"
            className="bg-blue-600 text-white p-3 rounded hover:bg-blue-700"
          >
            Publish Post
          </button>
        </form>
      )}

      {/* Posts List */}
      <div className="flex flex-col gap-4">
        {posts.length === 0 && (
          <p className="text-gray-500 text-center">No posts yet!</p>
        )}
        {posts.map((post) => (
          <div key={post.id} className="bg-white p-6 rounded shadow">
            <div className="flex justify-between items-start">
              <h3 className="text-xl font-bold mb-2">{post.title}</h3>
              {token && (
                <button
                  onClick={() => deletePost(post.id)}
                  className="text-red-500 hover:text-red-700 font-bold"
                >
                  ✕
                </button>
              )}
            </div>
            <p className="text-gray-600">{post.content}</p>
            <p className="text-sm text-gray-400 mt-3">
              {new Date(post.created_at).toLocaleDateString()}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Blog;