This software gives book recommendations based on a data set of ratings 1.200.000 ratings from 279.000 users on 271.000 books. The algorithms used are collaborative filtering, item based, user based and association rules.

The different algorithms can be executed from the folder [recommender/test/](https://github.com/xsergiolpx/Books-Recommender-System/tree/master/recommender/test). For example:

```
python test_all_with_cv.py list.txt
```

Where list.txt is a file that cointains one ISBN of one book on each row. The output will be recommended books by each recommended system based on the input list.
