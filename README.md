**Colorembo is a program for extracting colors from text**

If you create an embedding of the word "banana", as well as embeddings of the names of various colors, then in general, random colors will be close to the word "banana", and not "yellow" or "green". This program modifies the embedding space so that the closest to the word "banana" are its own colors, that is, "yellow" or "green".

**Idea**

In regular vector search, the L2 distance between two vectors is used, which for normalized vectors is calculated simply as the dot product. Colorembo, on the other hand, does the dot product not of two vectors, but of three: banana, color, and mask. The program's interface is built around searching for this very mask.

As training data, a color palette located on a plane is used, where the colors are the names of these colors in 4 languages. This palette is visible when you start the program.

As test data, a separate palette is used, on which the names of things that have a standard color are placed: a rose, jeans, a frog, etc. It can be seen if the argument True is passed to the initialization of the Store() class in the Dot function init class, located in interface_main.py

During mask training, the score is output to the terminal - the percentage of items from the test palette whose color was correctly determined when calculating through the trained mask.

The graphical interface is needed in order to visually determine how well the training words have approached the target palette.

**Why is this cool**

The mask can be interpreted as an embedding - it is the same vector of the same dimension. And this means that it can be inverted and get text in a natural language.

This text is essentially a spell that modifies the embedding space! Such a vector space spellcasting technique can be useful when working with vector databases. The spell allows you to clarify in what sense the vectors should be similar. In the case of Colorembo, this is the similarity of things in terms of their color.

**How to run the program**

The program is launched from the interface_main script. Training is started using the > button.

**Buttons**

o+ - add a new node. For correct operation, you need to add the openai key to the get_embedding.py module

o- - delete node

/+ - add edge

/- - delete edge

'>' start training

// - connect node with all others

-- - disconnect node from all others

dtt - connect all nodes with all others
