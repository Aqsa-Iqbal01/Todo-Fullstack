import React from 'react';
import TodoCard from './TodoCard';

interface Todo {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  due_date: string | null;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface TodoListProps {
  todos: Todo[];
  onEdit: (todo: Todo) => void;
  onDelete: (id: string) => void;
  onToggle: (id: string) => void;
}

const TodoList: React.FC<TodoListProps> = ({ todos, onEdit, onDelete, onToggle }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 gap-8">
      {todos.map((todo, index) => (
        <div
          key={todo.id}
          className="transform transition-all duration-300 hover:scale-[1.02] animate-fade-in"
          style={{ animationDelay: `${index * 50}ms` }}
        >
          <TodoCard
            todo={todo}
            onEdit={onEdit}
            onDelete={onDelete}
            onToggle={onToggle}
          />
        </div>
      ))}
    </div>
  );
};

export default TodoList;