#!/usr/bin/env -S stack runghc

import Control.Monad
import System.Console.ANSI
import System.Environment
import System.Process

runCommandOpts c = (\s -> if null s then s else init s) <$> readProcess "git" c []
putError s = do 
  setSGR [SetColor Foreground Vivid Red]
  putStrLn s
  setSGR [Reset]

main = do
  args <- getArgs
  let extractFile ix = if length args > ix then Just (args !! 1) else Nothing
  let fileName = case args of
                   ("ls" : opFile) -> extractFile 1
                   ("to" : _ : opFile) -> extractFile 2
  let options = maybe id (\n -> (++ [n])) fileName ["log", "--all", "--pretty=oneline"]
  destinations <-fmap (break (== ' '))  . lines <$> runCommandOpts options
  currentCommit <- runCommandOpts ["rev-parse", "HEAD"]
  if null destinations 
    then putError "The file is not tracked."
  else
    if args !! 0 == "ls"
      then
        forM_ (zip destinations [0..]) $ \ ((h, d), i) -> do
          setSGR [SetColor Foreground Vivid Green]
          putStr $ if h == currentCommit then "✓" else " "
          putStr $ show (i :: Int)
          setSGR [SetColor Foreground Vivid Yellow]
          putStr $ "    " ++ take 7 h ++ "    "
          setSGR [Reset]
          putStrLn d
      else do
        let index = read (args !! 1) :: Int
        if 0 <= index && index < length destinations 
          then do
            let (h, d) = destinations !! index
            runCommandOpts ["checkout", h]
            putStr "Switched to "
            setSGR [SetColor Foreground Vivid Green]
            putStr $ show index
            setSGR [SetColor Foreground Vivid Yellow]
            putStr $ " " ++ take 7 h ++ ""
            setSGR [Reset]
            putStrLn d
          else putError $ "Invalid index: " ++ show index

