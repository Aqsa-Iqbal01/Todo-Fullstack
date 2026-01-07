import React from 'react';

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

interface TodoCardProps {
  todo: Todo;
  onEdit: (todo: Todo) => void;
  onDelete: (id: string) => void;
  onToggle: (id: string) => void;
}

const TodoCard: React.FC<TodoCardProps> = ({ todo, onEdit, onDelete, onToggle }) => {
  const handleToggle = () => {
    onToggle(todo.id);
  };

  const handleEdit = () => {
    onEdit(todo);
  };

  const handleDelete = () => {
    onDelete(todo.id);
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  return (
    <div className={`rounded-2xl shadow-lg p-4 border-l-4 backdrop-blur-sm bg-white/30 dark:bg-gray-800/30 bg-gradient-to-br transform transition-all duration-300 hover:shadow-xl hover:-translate-y-1 ${
      todo.completed
        ? 'border-green-500 dark:border-green-600 from-green-50/50 to-emerald-50/50 dark:from-green-900/20 dark:to-emerald-900/20'
        : 'border-indigo-500 dark:border-indigo-600 from-blue-50/50 to-indigo-50/50 dark:from-indigo-900/20 dark:to-indigo-900/20'
    }`}>
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-start space-x-2">
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={handleToggle}
              className="sr-only"
              id={`toggle-${todo.id}`}
            />
            <label
              htmlFor={`toggle-${todo.id}`}
              className={`flex-shrink-0 mt-1 cursor-pointer rounded-full w-6 h-6 flex items-center justify-center transition-colors duration-300 ${
                todo.completed
                  ? 'bg-green-500 dark:bg-green-600 shadow-md'
                  : 'bg-gray-300 dark:bg-gray-600 border-2 border-dashed border-gray-400 dark:border-gray-500 shadow-md'
              }`}
            >
              {todo.completed && (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-white" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              )}
            </label>
            <div className="flex flex-col flex-1 min-w-0">
              <div className="flex items-center space-x-2 min-w-0 flex-1">
                <h3 className={`text-lg font-semibold min-w-0 truncate ${
                  todo.completed
                    ? 'line-through text-gray-600 dark:text-gray-400 decoration-gray-400 dark:decoration-gray-500'
                    : 'text-gray-800 dark:text-gray-200'
                }`}>
                  {todo.title}
                </h3>
                <span className={`px-2 py-1 text-xs font-semibold rounded-full flex-shrink-0 ${
                  todo.completed
                    ? 'bg-green-200 dark:bg-green-900/50 text-green-800 dark:text-green-200'
                    : 'bg-yellow-200 dark:bg-yellow-900/50 text-yellow-800 dark:text-yellow-200'
                }`}>
                  {todo.completed ? 'Complete' : 'Pending'}
                </span>
                <div className="flex space-x-1">
                  <button
                    onClick={handleEdit}
                    className={`p-1.5 rounded-lg transition-all duration-200 hover:scale-110 ${
                      todo.completed
                        ? 'text-green-600 dark:text-green-400 hover:text-green-800 dark:hover:text-green-300 hover:bg-green-100 dark:hover:bg-green-800/50 shadow-sm'
                        : 'text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 hover:bg-indigo-100 dark:hover:bg-indigo-800/50 shadow-sm'
                    }`}
                    aria-label="Edit"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                    </svg>
                  </button>
                  <button
                    onClick={handleDelete}
                    className={`p-1.5 rounded-lg transition-all duration-200 hover:scale-110 flex-shrink-0 ${
                      todo.completed
                        ? 'text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 hover:bg-red-100 dark:hover:bg-red-800/50 shadow-sm'
                        : 'text-red-700 dark:text-red-400 hover:text-red-900 dark:hover:text-red-300 hover:bg-red-100 dark:hover:bg-red-800/50 shadow-sm'
                    }`}
                    aria-label="Delete"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
          {todo.description && (
            <p className={`mt-2 text-sm ${
              todo.completed
                ? 'text-gray-500 dark:text-gray-400'
                : 'text-gray-600 dark:text-gray-300'
            }`}>
              {todo.description}
            </p>
          )}
        </div>
      </div>

      <div className="flex items-center justify-between mt-4 pt-3 border-t border-gray-200/50 dark:border-gray-700/50">
        {todo.due_date && (
          <div className="flex items-center">
            <div className={`p-2 rounded-lg ${
              todo.completed
                ? 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400'
                : 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
            }`}>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <span className={`ml-2 text-xs font-medium ${
              todo.completed
                ? 'text-green-700 dark:text-green-400'
                : 'text-blue-700 dark:text-blue-400'
            }`}>
              Due: {formatDate(todo.due_date)}
            </span>
          </div>
        )}

        <div className="text-xs text-gray-500 dark:text-gray-400">
          {formatDate(todo.created_at)}
        </div>
      </div>

      {todo.updated_at !== todo.created_at && (
        <div className="mt-2 text-xs text-gray-500 dark:text-gray-400 text-right">
          Updated: {formatDate(todo.updated_at)}
        </div>
      )}
    </div>
  );
};

export default TodoCard;