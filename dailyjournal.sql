CREATE TABLE `Mood` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `label` TEXT NOT NULL
)

CREATE TABLE `Entry` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `date`    TEXT NOT NULL,
    `concept`   TEXT NOT NULL,
    `text`    TEXT NOT NULL,
    `mood_id`   INT NOT NULL,
    FOREIGN KEY(`mood_id`) REFERENCES `Mood`(`id`)
);

INSERT INTO `Mood` VALUES (null, "Happy");
INSERT INTO `Mood` VALUES (null, "Sad");
INSERT INTO `Mood` VALUES (null, "Overwhelmed");
INSERT INTO `Mood` VALUES (null, "Excited");
INSERT INTO `Mood` VALUES (null, "Accomplished");
INSERT INTO `Mood` VALUES (null, "Caffeinated");
INSERT INTO `Mood` VALUES (null, "Sleepy");
INSERT INTO `Mood` VALUES (null, "Exhausted");
INSERT INTO `Mood` VALUES (null, "Proud");

INSERT INTO `Entry` VALUES (null, "1/8/2021", "HTML", "Today we learned HTML. It was easy and fun.", 1);
INSERT INTO `Entry` VALUES (null, "1/31/2021", "CSS", "CSS is the most fun! I love styling sites.", 4);
INSERT INTO `Entry` VALUES (null, "2/6/2021", "JavaScript", "JavaScript is hard to understand, but I think I'm getting it.", 3);
INSERT INTO `Entry` VALUES (null, "3/10/2021", "React", "We worked with React today and it was hard. It is awesome, too.", 6);

SELECT * FROM Entry