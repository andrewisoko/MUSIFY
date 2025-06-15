import React from 'react';
import './App.css';
import Home from './components/Home';
import Playlists from '../pages/Playlists';
import { Routes,Route } from 'react-router-dom';


const App = () => {
  return (
      <Routes>
        <Route path ="/" element ={<Home/>}></Route>
         <Route path="/playlists" element={<Playlists />} />
      </Routes>
      
  );
};

export default App;