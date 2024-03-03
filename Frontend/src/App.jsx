import { useState } from 'react'
import './App.css'
import axios from 'axios';
import loader from "./loader.png"; 
import github from "./github.png";

const Home = () => {
  const [sentence, setSentence] = useState('');
  const [sentimentScore, setSentimentScore] = useState(null);
  const [sentiment, setSentiment] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isEmpty, setIsEmpty] = useState(true);

  const handleSubmit = async () => {
    if (!sentence.trim()) {
      return;
    }

    setIsLoading(true);
    try {
      const response = await axios.get(`https://fastapi-production-8770.up.railway.app/predict?sentence=${encodeURIComponent(sentence)}`);
      const { sentiment_score, sentiment } = response.data;
      setSentimentScore(sentiment_score);
      setSentiment(sentiment);
    } catch (error) {
      console.error('Error fetching sentiment score:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e) => {
    setSentence(e.target.value);
    setIsEmpty(e.target.value.trim() === '');
  };

  const handleClear = () => {
    setSentence('');
    setSentimentScore(null);
    setSentiment(null);
    setIsEmpty(true);
  };

  // Array of suggestions
  const suggestions = ["Mehsulu chox beyendim", "Servis seviyyesi chox ashagidir"];

  const handleSuggestionClick = (suggestion) => {
    setSentence(suggestion);
    setIsEmpty(false); // Setting to false since suggestion is not empty
  };

  return (
    <div className="container mx-auto py-8 px-4 sm:px-8 md:px-16 lg:px-24 xl:px-32">
      <h1 className="text-4xl font-bold text-blue-600 mb-4 text-center">Sentiment Analysis in Azerbaijani Language</h1>
      <div className='author my-4 text-center text-sm'>
        <p className= "text-sm">
          Made by Kamal Ahmadov
        </p>
        <a href="https://github.com/Kamal578/SentimentAnalysis" target="_blank" rel="noreferrer" className='flex items-center justify-center gap-2 hover:text-bold'>
          <img src={github} alt="github" className="w-6 h-6" /> Source Code
        </a>
      </div>
      <div className="flex flex-col items-center justify-center gap-4">
        <textarea
          className="transition-all w-full sm:w-[75%] md:w-[60%] lg:w-[50%] h-32 border border-gray-300 rounded-md px-4 py-2 mb-4 resize-none focus:outline-none focus:ring focus:border-blue-200"
          placeholder="Enter your sentence..."
          value={sentence}
          onChange={handleInputChange}
        />
        <p className="text-gray-500 text-sm text-center">You may try these examples</p>
        <div className="suggestions flex flex-col sm:flex-row gap-2 justify-center items-center">
          {suggestions.map((suggestion, index) => (
            <button
              key={index}
              className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-2 rounded transition duration-300 ease-in-out"
              onClick={() => handleSuggestionClick(suggestion)}
            >
              {suggestion}
            </button>
          ))}
        </div>
        <div className='buttons flex flex-col sm:flex-row gap-4 items-center justify-center'>
          <button
            className={`bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-6 rounded transition duration-300 ease-in-out ${isEmpty ? 'cursor-not-allowed opacity-50' : ''
              }`}
            onClick={handleSubmit}
            disabled={isEmpty}
          >
            {isLoading ? (
              <span className='flex items-center'>
                <span>Loading...</span>
                <div className="animate-spin h-5 w-5 border-white ml-2">
                  <img src={loader} alt="loading" />
                </div>
              </span>
            ) : (
              'Analyze'
            )}
          </button>
          <button
            className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-6 rounded transition duration-300 ease-in-out mt-2 sm:mt-0"
            onClick={handleClear}
          >
            Clear
          </button>
        </div>
      </div>
      {sentimentScore !== null && (
        <div className="mt-4 text-center">
          <div className='flex justify-center items-center gap-1 flex-row'>
            <p className="font-semibold text-lg">Sentiment Score:</p>
            <p className="text-xl font-bold">{sentimentScore.toFixed(3)}</p>
          </div>
          <div className='flex justify-center items-center gap-1 flex-row'>
            <p className="font-semibold text-lg">Tone:</p>
            <p className={`text-lg font-bold uppercase ${sentimentScore && sentimentScore > 0.5 ? 'text-green-600' : 'text-red-600'}`}>
              {sentiment}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;
