import React from 'react';
import Header from '../components/Header';
import VideoForm from '../components/VideoForm';

const HomePage = () => {
  return (
    <div>
      <Header />
      <div className="max-w-2xl mx-auto mt-10">
        <VideoForm />
      </div>
    </div>
  );
};

export default HomePage;
