-- ref.: https://github.com/aparrish/rwet/blob/master/ngrams-and-markov-chains.ipynb
main = return ()

slice :: Int -> Int -> [a] -> [a]
slice from to list = take (to - from) $ drop from list

join :: a -> [[a]] -> [a]
join delim [x] = x
join delim (x:xs) = x ++ [delim] ++ (join delim xs)

split :: Eq a => a -> [a] -> [[a]]
split delim [] = [[]]
split delim (x:xs)
    | delim == x = [] : rest
    | otherwise = (x : head rest) : tail rest
    where
        rest = split delim xs


ngrams :: Int -> [a] -> [[a]]
ngrams n list = [slice i (i+n) list | i <- [0 .. (length list - n)]]

pairs :: String -> [(String, String)]
pairs text = let wrds = words text in
    [(wrds !! i, wrds !! (i+1)) | i <- [0 .. (length wrds - 2)]]


-- ngrams 2 "condescendences": 
-- >>> ["condescendences"[i:i+2] for i in range(len("condescendences")-1)]

-- s = "Two roads diverged in a yellow wood, And sorry I"
-- v = split ' ' s
-- >>> v = s.split(' ')

-- ngrams 5 v:
-- >>> [' '.join(v[i:i+5]) for i in range(len(v) - 4)]

-- map (\x -> length x) $ ngrams 5 v
-- >>> list(map(lambda x: len(x), v))

--def ngram_to_next_dict(src, order, model={}):
--    src += '$'
--    for i in range(len(src) - order):
--        ngram = tuple(src[i : i+order])
--        next = src[i + order]
--        try: 
--            model[ngram].append(next)
--        except: 
--            model[ngram] = [next]
--    return model