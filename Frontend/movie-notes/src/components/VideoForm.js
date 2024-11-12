import React, { useState } from 'react';

const VideoForm = () => {
  const [url, setUrl] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Submitted URL: ', url);
    // Here, you’d send the URL to your backend.
  };

  return (
    <form onSubmit={handleSubmit} className="p-4">
      <label className="block text-gray-700 text-sm font-bold mb-2">
        YouTube Video URL:
      </label>
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
      />
      <button
        type="submit"
        className="bg-blue-500 text-white mt-4 px-4 py-2 rounded hover:bg-blue-600"
      >
        Transcribe
      </button>
    </form>
  );
};

export default VideoForm;
