import React from 'react';
import './App.css';
import Home from './components/Home';
import { Routes,Route } from 'react-router-dom';


const App = () => {
  return (
      <Routes>
        <Route path ="/" element ={<Home/>}></Route>
      </Routes>
      
  );
};

export default App;