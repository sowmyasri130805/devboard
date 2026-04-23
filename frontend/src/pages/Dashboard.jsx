import { useState, useEffect } from "react";
import API from "../api";

function Dashboard() {
  const [todos, setTodos] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      const res = await API.get("/todos/");
      setTodos(res.data);
    } catch (err) {
      console.error("Error fetching todos", err);
    }
  };

  const createTodo = async (e) => {
    e.preventDefault();
    try {
      await API.post("/todos/", { title, description });
      setTitle("");
      setDescription("");
      fetchTodos();
    } catch (err) {
      console.error("Error creating todo", err);
    }
  };

  const toggleComplete = async (todo) => {
    await API.patch(`/todos/${todo.id}`, { completed: !todo.completed });
    fetchTodos();
  };

  const deleteTodo = async (id) => {
    await API.delete(`/todos/${id}`);
    fetchTodos();
  };

  return (
    <div className="mt-8">
      <h2 className="text-2xl font-bold mb-6">My Todos 📝</h2>

      {/* Create Todo Form */}
      <form
        onSubmit={createTodo}
        className="bg-white p-6 rounded shadow mb-6 flex flex-col gap-3"
      >
        <input
          type="text"
          placeholder="Todo title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="border p-3 rounded"
          required
        />
        <input
          type="text"
          placeholder="Description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="border p-3 rounded"
        />
        <button
          type="submit"
          className="bg-blue-600 text-white p-3 rounded hover:bg-blue-700"
        >
          Add Todo
        </button>
      </form>

      {/* Todo List */}
      <div className="flex flex-col gap-3">
        {todos.length === 0 && (
          <p className="text-gray-500 text-center">
            No todos yet! Add one above.
          </p>
        )}
        {todos.map((todo) => (
          <div
            key={todo.id}
            className="bg-white p-4 rounded shadow flex justify-between items-center"
          >
            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => toggleComplete(todo)}
                className="w-5 h-5 cursor-pointer"
              />
              <div>
                <p
                  className={`font-medium ${
                    todo.completed ? "line-through text-gray-400" : ""
                  }`}
                >
                  {todo.title}
                </p>
                {todo.description && (
                  <p className="text-sm text-gray-500">{todo.description}</p>
                )}
              </div>
            </div>
            <button
              onClick={() => deleteTodo(todo.id)}
              className="text-red-500 hover:text-red-700 font-bold text-lg"
            >
              ✕
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Dashboard;