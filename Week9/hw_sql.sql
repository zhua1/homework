USE sakila;

/* 1a. You need a list of all the actors who have Display the first and
 * last names of all actors from the table `actor`.
 */
SELECT *
FROM actor;

/* 1b. Display the first and last name of each actor in a single column
 * in upper case letters. Name the column `Actor Name`.
 */
SELECT first_name, last_name
FROM actor;

/* 2a. You need to find the ID number, first name, and last name of an actor, 
 * of whom you know only the first name, "Joe." What is one query would
 * you use to obtain this information?
 */
SELECT actor_id, first_name, last_name
FROM actor
WHERE first_name = 'Joe';

/* 2b. Find all actors whose last name contain the letters `GEN`: */
SELECT first_name, last_name
FROM actor
WHERE last_name LIKE '%GEN%';

/* 2c. Find all actors whose last names contain the letters `LI`. 
 * This time, order the rows by last name and first name, in that order:
 */
SELECT first_name, last_name
FROM actor
WHERE last_name LIKE '%LI%'
ORDER BY last_name, first_name;

/* 2d. Using `IN`, display the `country_id` and `country` columns 
 * of the following countries: Afghanistan, Bangladesh, and China:
 */
SELECT country_id, country
FROM country
WHERE country_id
IN (1, 12, 23);

/* 3a. Add a `middle_name` column to the table `actor`. Position it between `first_name` and `last_name`. 
 * Hint: you will need to specify the data type.
 */
ALTER TABLE actor ADD middle_name VARCHAR(60) AFTER first_name;

/* 3b. You realize that some of these actors have tremendously long last names. 
 * Change the data type of the `middle_name` column to `blobs`.
 */
ALTER TABLE actor MODIFY COLUMN middle_name BLOB;

/* 3c. Now delete the `middle_name` column. */
ALTER TABLE actor DROP COLUMN middle_name;

/* 4a. List the last names of actors, as well as how many actors have that last name. */
SELECT last_name, COUNT(*) AS 'number_of_people'
FROM actor
GROUP BY last_name;

/* 4b. List last names of actors and the number of actors who have that last name, 
 * but only for names that are shared by at least two actors
 */
SELECT last_name, COUNT(*) AS 'number_of_people'
FROM actor
GROUP BY last_name
HAVING number_of_people >= 2; 

/* 4c. Oh, no! The actor `HARPO WILLIAMS` was accidentally entered in the `actor` table as `GROUCHO WILLIAMS`, 
 * the name of Harpo's second cousin's husband's yoga teacher. Write a query to fix the record.
 */
UPDATE actor
SET first_name = 'HARPO'
WHERE first_name = 'GROUCHO' AND last_name = 'WILLIAMS';

/* 4d. Perhaps we were too hasty in changing `GROUCHO` to `HARPO`. 
 * It turns out that `GROUCHO` was the correct name after all! In a single query, 
 * if the first name of the actor is currently `HARPO`, change it to `GROUCHO`. 
 * Otherwise, change the first name to `MUCHO GROUCHO`, as that is exactly what the actor 
 * will be with the grievous error. BE CAREFUL NOT TO CHANGE THE FIRST NAME OF EVERY ACTOR 
 * TO `MUCHO GROUCHO`, HOWEVER! (Hint: update the record using a unique identifier.)
 */
UPDATE actor
SET first_name = 
(CASE
   WHEN first_name = 'HARPO' THEN 'GROUCHO'
   ELSE 'MUCHO GROUCHO'
END)
WHERE actor_id = 172;

/* 5a. You cannot locate the schema of the `address` table. Which query would you use to re-create it? */
SELECT *
FROM address;

/* 6a. Use `JOIN` to display the first and last names, as well as the address, 
 * of each staff member. Use the tables `staff` and `address`:
 */
SELECT s.first_name, s.last_name, a.address
FROM staff AS s
JOIN address AS a
USING (address_id);

/* 6b. Use `JOIN` to display the total amount rung up by each staff member in August of 2005. 
 * Use tables `staff` and `payment`. 
 */
SELECT s.staff_id, s.first_name, s.last_name, SUM(p.amount) AS 'total_spent'
FROM staff as s
JOIN payment as p 
USING (staff_id)
GROUP BY staff_id;

/* 6c. List each film and the number of actors who are listed for that film. 
 * Use tables `film_actor` and `film`. Use inner join. 
 */
SELECT title, COUNT(actor_id)
FROM film
INNER JOIN film_actor
USING (film_id)
GROUP BY title; 
 
/* 6d. How many copies of the film `Hunchback Impossible` exist in the inventory system? */
SELECT COUNT(*) AS '# of copies'
FROM inventory
WHERE film_id
IN (
	SELECT film_id
	FROM film
	WHERE title = 'Hunchback Impossible'
);

/* 6e. Using the tables `payment` and `customer` and the `JOIN` command, 
 * list the total paid by each customer. List the customers alphabetically by last name: 
 */
SELECT c.customer_id, c.first_name, c.last_name, SUM(p.amount) AS 'total_spent'
FROM payment AS p
JOIN customer AS c
USING (customer_id)
GROUP BY customer_id
ORDER BY c.last_name;

/* 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. 
 * As an unintended consequence, films starting with the letters `K` and `Q` have also soared in popularity. 
 * Use subqueries to display the titles of movies starting with the letters `K` and `Q` whose language is English.  
 */
SELECT title
FROM film
WHERE title LIKE 'K%' OR title LIKE 'Q%'
AND language_id 
IN (
	SELECT language_id
	FROM language
	WHERE name = 'English'
);

/* 7b. Use subqueries to display all actors who appear in the film `Alone Trip`. */
SELECT first_name, last_name
FROM actor
WHERE actor_id
IN (
	SELECT actor_id
	FROM film_actor
	WHERE film_id 
	IN (
		SELECT film_id
		FROM film
		WHERE title = 'Alone Trip'
	)
);

/* 7c. You want to run an email marketing campaign in Canada, for which you will need the names 
 * and email addresses of all Canadian customers. Use joins to retrieve this information. */
SELECT first_name, last_name, email
FROM customer
WHERE address_id
IN (
	SELECT address_id
	FROM address
	WHERE city_id
	IN (
		SELECT city_id
		FROM city
		INNER JOIN country
		USING (country_id)
		WHERE country_id
		IN (
			SELECT country_id
			FROM country
			WHERE country = 'Canada'
		)
	)
);

/* 7d. Sales have been lagging among young families, and you wish to target all family movies 
 * for a promotion. Identify all movies categorized as famiy films. */
 
 