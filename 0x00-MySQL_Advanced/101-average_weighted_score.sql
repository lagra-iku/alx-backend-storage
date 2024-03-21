-- a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    DECLARE average_score FLOAT;
    
    DECLARE user_cursor CURSOR FOR 
        SELECT DISTINCT id
        FROM users;
        
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN user_cursor;
    
    user_loop: LOOP
        -- Fetch the next user ID
        FETCH user_cursor INTO user_id;
        
        IF done THEN
            LEAVE user_loop;
        END IF;
        
        SELECT SUM(score * weight) INTO total_score
        FROM scores
        WHERE user_id = user_id;
        
        SELECT SUM(weight) INTO total_weight
        FROM scores
        WHERE user_id = user_id;
        
        IF total_weight > 0 THEN
            SET average_score = total_score / total_weight;
        ELSE
            SET average_score = 0;
        END IF;
        
        UPDATE users
        SET average_weighted_score = average_score
        WHERE id = user_id;
    END LOOP;
    
    CLOSE user_cursor;
    
END //

DELIMITER ;
