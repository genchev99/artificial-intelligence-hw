[Играта](https://appzaza.com/tile-slide-game) започва с квадратна дъска, състояща се от плочки с номера от 1 до N и една
празна плочка, представена с цифрата 0. Целта е да се наредят плочките в съответствие с техните номера. Местенето се
извършва, като на мястото на празната плочка могат да се преместят плочки отгоре, отдолу, отляво и отдясно.

На входа се подава число N - броя на плочките с номера (8, 15, 24 и т.н.), число I - индексът на позицията на нулата в
решението (при -1 се задава индекс по подразбиране - най-долу в дясно) и след това се въвежда подредбата на дъската. С
помощта на алгоритъма IDА* и евристиката "разстояние на Манхатън" да се изведе:

1. На първият ред дължината на "оптималния" път от началото до целевото състояние.
1. Съответните стъпки (на нов ред за всяка една), които се извършват за да се стигне до крайното състояние. Стъпките са
   left, right, up и down

> Имайте предвид, че не всяка конфигурация на входен пъзел, която подадете, е решима. Дали пъзелът е решим може да се провери като обяснения как това може да се направи могат да бъдат намерини [тук](https://www.cs.princeton.edu/courses/archive/spring18/cos226/assignments/8puzzle/index.html).

> Моля, принтирайте времето необходимо за намиране на пътя (без да включвате времето за принтиране на решението) в секунди с точност поне до 2-рия знак след нулата.

###### Примерен вход:

> 8
>
> -1
>
> 1 2 3 4 5 6 0 7 8

###### Примерен изход:

> 2
>
> left
>
> left