-- a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    DECLARE average_score FLOAT;
    
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
END //
DELIMITER ;
