import { useState } from "react";
import { motion } from "framer-motion";
import axios from "axios";
import "./App.css";
import { PlaceholdersAndVanishInput } from "./components/inputThingy";

function App() {
  const placeholders = [
    "What's the first rule of Fight Club?",
    "Who is Tyler Durden?",
    "Where is Andrew Laeddis Hiding?",
    "Write a Javascript method to reverse a string",
    "How to assemble your own PC?",
  ];

  const [dreamDescription, setDreamDescription] = useState("");
  const [result, setResult] = useState(null);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDreamDescription(e.target.value);
  };

  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsSubmitted(true);
    try {
      const response = await axios.post("/api/interpret", {
        description: dreamDescription,
      });

      setResult(response.data);

      console.log("Dream interpreted:", response.data);
    } catch (error) {
      console.error("Error interpreting the dream:", error);
      setResult({ error: "Could not interpret the dream. Try again later." });
    }
  };

  return (
    <div className="h-[40rem] flex flex-col justify-center items-center px-4">
      <h2 className="mb-10 sm:mb-20 text-xl text-center sm:text-5xl dark:text-gray-500 text-black">
        What do you dream of?
      </h2>
      {!isSubmitted ? (
        <PlaceholdersAndVanishInput
          placeholders={placeholders}
          onChange={handleChange}
          onSubmit={onSubmit}
        />
      ) : (
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col items-center space-y-4"
        >
          {result && !result.error ? (
            <>
              <h3 className="text-2xl font-bold">Dream Symbol:</h3>
              <p className="text-lg">{result.symbol}</p>
              <h3 className="text-2xl font-bold">Interpretation:</h3>
              <p className="text-lg">{result.interpretation}</p>
            </>
          ) : (
            <p className="text-red-500">{result?.error}</p>
          )}
        </motion.div>
      )}
    </div>
  );
}

export default App;
