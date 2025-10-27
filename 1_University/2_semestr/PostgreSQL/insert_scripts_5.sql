INSERT INTO emp_pos_relation (fk_employee, fk_position, percentage) VALUES

-- Management positions
(1, 1, 100),  -- Akira Tanaka - CEO
(2, 2, 100),  -- Yuki Nakamura - CTO
(3, 3, 100),  -- Takeshi Yamamoto - CFO
(4, 4, 100),  -- Haruka Sato - COO
(5, 5, 100),  -- Kenji Watanabe - CMO
(6, 6, 100),  -- Aiko Suzuki - Director of HR
(7, 7, 100),  -- Daisuke Ito - Director of Sales

-- Software Development positions
(8, 8, 100),   -- Emi Kobayashi - Lead Software Architect
(9, 9, 100),   -- Hiroshi Kato - Senior Developer
(10, 9, 100),  -- Miyuki Yamaguchi - Senior Developer

-- Employees with multiple positions (split percentages)
(11, 9, 60),   -- Takahiro Saito - Senior Developer (60%)
(11, 12, 40),  -- Takahiro Saito - Data Science Manager (40%)

(12, 10, 100), -- Sakura Kimura - Junior Developer
(13, 10, 100), -- Kazuki Hashimoto - Junior Developer
(14, 10, 100), -- Yumiko Inoue - Junior Developer
(15, 11, 100), -- Ryo Hayashi - QA Engineer

-- Another employee with multiple positions
(16, 11, 70),  -- Nanami Takahashi - QA Engineer (70%)
(16, 10, 30),  -- Nanami Takahashi - Junior Developer (30%)

-- Data Science and Analytics
(17, 12, 100), -- Toshiro Mori - Data Science Manager
(18, 13, 100), -- Akane Ikeda - Data Scientist
(19, 13, 100), -- Yasuhiro Matsuda - Data Scientist

-- Another employee with multiple positions
(20, 14, 80),  -- Hina Fujita - Data Analyst (80%)
(20, 13, 20),  -- Hina Fujita - Data Scientist (20%)

(21, 14, 100), -- Satoshi Aoki - Data Analyst

-- Design Team
(22, 15, 100), -- Hana Yamada - UX/UI Design Lead
(23, 16, 100), -- Jiro Sasaki - Senior Designer

-- Another employee with multiple positions
(24, 17, 60),  -- Misaki Miyazaki - Junior Designer (60%)
(24, 18, 40),  -- Misaki Miyazaki - Graphic Designer (40%)

(25, 18, 100), -- Yoshiro Fukuda - Graphic Designer

-- Marketing Team
(26, 19, 100), -- Kiyomi Abe - Marketing Manager
(27, 20, 100), -- Daiki Yoshida - Digital Marketing Specialist

-- Rare case of employee with 3 positions
(28, 21, 40),  -- Rin Ishikawa - Content Creator (40%)
(28, 22, 30),  -- Rin Ishikawa - SEO Specialist (30%)
(28, 23, 30),  -- Rin Ishikawa - Social Media Manager (30%)

(29, 22, 100), -- Kazuo Okada - SEO Specialist
(30, 23, 100), -- Miyu Goto - Social Media Manager

-- HR Team
(31, 24, 100), -- Kenta Shimizu - HR Manager
(32, 25, 100), -- Yuna Taniguchi - Recruitment Specialist
(33, 26, 100), -- Shinji Kawaguchi - HR Assistant

-- Finance Team
(34, 27, 100), -- Asuka Nomura - Finance Manager
(35, 28, 100), -- Takuma Sugiyama - Accountant

-- Another employee with multiple positions
(36, 29, 70),  -- Haru Nakajima - Financial Analyst (70%)
(36, 28, 30),  -- Haru Nakajima - Accountant (30%)

-- Sales Team
(37, 30, 100), -- Ryota Takeuchi - Sales Manager
(38, 31, 100), -- Momoko Aoyama - Sales Representative
(39, 31, 100), -- Yusuke Maeda - Sales Representative
(40, 31, 100), -- Rika Yoshimura - Sales Representative

-- IT Support
(41, 32, 100), -- Naoki Matsumoto - IT Support Manager
(42, 33, 100), -- Ayumi Hasegawa - IT Support Specialist

-- Another rare case with 3 positions
(43, 33, 50),  -- Koji Oyama - IT Support Specialist (50%)
(43, 10, 30),  -- Koji Oyama - Junior Developer (30%)
(43, 11, 20),  -- Koji Oyama - QA Engineer (20%)

-- Customer Support
(44, 34, 100), -- Saki Ueda - Customer Support Manager
(45, 35, 100), -- Hideo Kurosawa - Customer Support Specialist
(46, 35, 100), -- Natsumi Imai - Customer Support Specialist

-- Another employee with multiple positions
(47, 35, 60),  -- Kenichi Takeda - Customer Support Specialist (60%)
(47, 21, 40),  -- Kenichi Takeda - Content Creator (40%)

-- Product Management
(48, 36, 100), -- Miki Okamoto - Product Manager
(49, 37, 100), -- Toru Murata - Product Owner
(50, 38, 100), -- Risa Sakamoto - Product Analyst

-- Continuing with more employees and positions...
-- Employees 51-100 - mix of single and multi-position employees

(51, 9, 100),   -- Senior Developer
(52, 16, 100),  -- Senior Designer
(53, 27, 100),  -- Finance Manager
(54, 21, 100),  -- Content Creator
(55, 12, 100),  -- Data Science Manager
(56, 10, 100),  -- Junior Developer
(57, 14, 100),  -- Data Analyst
(58, 17, 100),  -- Junior Designer

-- Another employee with multiple positions
(59, 9, 70),    -- Senior Developer (70%)
(59, 8, 30),    -- Lead Software Architect (30%)

(60, 35, 100),  -- Customer Support Specialist

-- Employees with multiple positions
(61, 30, 70),   -- Sales Manager (70%)
(61, 19, 30),   -- Marketing Manager (30%)

(62, 24, 100),  -- HR Manager
(63, 10, 100),  -- Junior Developer
(64, 35, 100),  -- Customer Support Specialist
(65, 9, 100),   -- Senior Developer
(66, 26, 100),  -- HR Assistant
(67, 10, 100),  -- Junior Developer

-- Another employee with multiple positions
(68, 17, 80),   -- Junior Designer (80%)
(68, 21, 20),   -- Content Creator (20%)

(69, 33, 100),  -- IT Support Specialist
(70, 21, 100),  -- Content Creator

-- Continuing pattern through the rest of employees
(71, 28, 100),  -- Accountant
(72, 35, 100),  -- Customer Support Specialist
(73, 9, 100),   -- Senior Developer
(74, 22, 100),  -- SEO Specialist
(75, 9, 100),   -- Senior Developer
(76, 17, 100),  -- Junior Designer
(77, 35, 100),  -- Customer Support Specialist
(78, 20, 100),  -- Digital Marketing Specialist
(79, 28, 100),  -- Accountant
(80, 14, 100),  -- Data Analyst

-- Continue with employees 81-400
-- Only showing some examples to save space, would continue pattern for all employees

(81, 10, 100),  -- Junior Developer
(82, 13, 100),  -- Data Scientist

-- Another employee with multiple positions
(83, 33, 60),   -- IT Support Specialist (60%)
(83, 32, 40),   -- IT Support Manager (40%)

(84, 26, 100),  -- HR Assistant
(85, 9, 100),   -- Senior Developer
(86, 35, 100),  -- Customer Support Specialist
(87, 10, 100),  -- Junior Developer
(88, 14, 100),  -- Data Analyst
(89, 31, 100),  -- Sales Representative

-- Another employee with 3 positions (rare)
(90, 20, 50),   -- Digital Marketing Specialist (50%)
(90, 22, 30),   -- SEO Specialist (30%) 
(90, 23, 20),   -- Social Media Manager (20%)
(91, 9, 100),   -- Senior Developer
(92, 17, 100),  -- Junior Designer
(93, 28, 100),  -- Accountant
(94, 35, 100),  -- Customer Support Specialist
(95, 33, 100),  -- IT Support Specialist
(96, 14, 100),  -- Data Analyst
(97, 31, 100),  -- Sales Representative
(98, 10, 100),  -- Junior Developer

-- Employee with multiple positions
(99, 19, 60),   -- Marketing Manager (60%)
(99, 20, 40),   -- Digital Marketing Specialist (40%)

(100, 13, 100), -- Data Scientist

-- Continue with employees 101-150
(101, 9, 100),  -- Senior Developer
(102, 25, 100), -- Recruitment Specialist
(103, 10, 100), -- Junior Developer
(104, 26, 100), -- HR Assistant
(105, 11, 100), -- QA Engineer

-- Employee with multiple positions
(106, 21, 70),  -- Content Creator (70%)
(106, 23, 30),  -- Social Media Manager (30%)

(107, 9, 100),  -- Senior Developer
(108, 35, 100), -- Customer Support Specialist
(109, 14, 100), -- Data Analyst
(110, 29, 100), -- Financial Analyst

-- Another employee with multiple positions
(111, 16, 80),  -- Senior Designer (80%)
(111, 15, 20),  -- UX/UI Design Lead (20%)

(112, 10, 100), -- Junior Developer
(113, 9, 100),  -- Senior Developer
(114, 34, 100), -- Customer Support Manager
(115, 31, 100), -- Sales Representative

-- Employee with triple position (rare)
(116, 10, 50),  -- Junior Developer (50%)
(116, 11, 30),  -- QA Engineer (30%)
(116, 33, 20),  -- IT Support Specialist (20%)

(117, 28, 100), -- Accountant
(118, 17, 100), -- Junior Designer
(119, 9, 100),  -- Senior Developer
(120, 35, 100), -- Customer Support Specialist

-- Continue with employees 121-150
(121, 31, 100), -- Sales Representative
(122, 10, 100), -- Junior Developer
(123, 22, 100), -- SEO Specialist
(124, 13, 100), -- Data Scientist
(125, 18, 100), -- Graphic Designer

-- Employee with multiple positions
(126, 9, 60),   -- Senior Developer (60%)
(126, 8, 40),   -- Lead Software Architect (40%)

(127, 20, 100), -- Digital Marketing Specialist
(128, 14, 100), -- Data Analyst
(129, 10, 100), -- Junior Developer
(130, 35, 100), -- Customer Support Specialist

-- Another employee with multiple positions
(131, 33, 75),  -- IT Support Specialist (75%)
(131, 32, 25),  -- IT Support Manager (25%)

(132, 10, 100), -- Junior Developer
(133, 28, 100), -- Accountant
(134, 35, 100), -- Customer Support Specialist
(135, 9, 100),  -- Senior Developer

-- Employee with multiple positions
(136, 17, 60),  -- Junior Designer (60%)
(136, 18, 40),  -- Graphic Designer (40%)

(137, 31, 100), -- Sales Representative
(138, 10, 100), -- Junior Developer
(139, 9, 100),  -- Senior Developer
(140, 26, 100), -- HR Assistant

-- Continue with employees 151-200
(141, 10, 100), -- Junior Developer
(142, 35, 100), -- Customer Support Specialist
(143, 9, 100),  -- Senior Developer
(144, 28, 100), -- Accountant
(145, 14, 100), -- Data Analyst

-- Employee with multiple positions
(146, 21, 65),  -- Content Creator (65%)
(146, 22, 35),  -- SEO Specialist (35%)

(147, 10, 100), -- Junior Developer
(148, 17, 100), -- Junior Designer
(149, 9, 100),  -- Senior Developer
(150, 13, 100), -- Data Scientist

-- Another employee with multiple positions
(151, 35, 80),  -- Customer Support Specialist (80%)
(151, 34, 20),  -- Customer Support Manager (20%)

(152, 10, 100), -- Junior Developer
(153, 31, 100), -- Sales Representative
(154, 11, 100), -- QA Engineer
(155, 9, 100),  -- Senior Developer

-- Employee with triple position (rare)
(156, 10, 40),  -- Junior Developer (40%)
(156, 11, 40),  -- QA Engineer (40%)
(156, 33, 20),  -- IT Support Specialist (20%)

(157, 28, 100), -- Accountant
(158, 35, 100), -- Customer Support Specialist
(159, 9, 100),  -- Senior Developer
(160, 20, 100), -- Digital Marketing Specialist

-- Employee with multiple positions
(161, 10, 70),  -- Junior Developer (70%)
(161, 11, 30),  -- QA Engineer (30%)

(162, 14, 100), -- Data Analyst
(163, 9, 100),  -- Senior Developer
(164, 35, 100), -- Customer Support Specialist
(165, 16, 100), -- Senior Designer

-- Employee with multiple positions
(166, 17, 50),  -- Junior Designer (50%)
(166, 18, 50),  -- Graphic Designer (50%)

(167, 21, 100), -- Content Creator
(168, 9, 100),  -- Senior Developer
(169, 10, 100), -- Junior Developer
(170, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(171, 33, 65),  -- IT Support Specialist (65%)
(171, 10, 35),  -- Junior Developer (35%)

(172, 28, 100), -- Accountant
(173, 9, 100),  -- Senior Developer
(174, 31, 100), -- Sales Representative
(175, 14, 100), -- Data Analyst

-- Employee with multiple positions
(176, 19, 75),  -- Marketing Manager (75%)
(176, 20, 25),  -- Digital Marketing Specialist (25%)

(177, 10, 100), -- Junior Developer
(178, 35, 100), -- Customer Support Specialist
(179, 9, 100),  -- Senior Developer
(180, 17, 100), -- Junior Designer

-- Employee with multiple positions
(181, 13, 60),  -- Data Scientist (60%)
(181, 12, 40),  -- Data Science Manager (40%)

(182, 28, 100), -- Accountant
(183, 10, 100), -- Junior Developer
(184, 35, 100), -- Customer Support Specialist
(185, 9, 100),  -- Senior Developer

-- Employee with multiple positions
(186, 18, 75),  -- Graphic Designer (75%)
(186, 17, 25),  -- Junior Designer (25%)

(187, 31, 100), -- Sales Representative
(188, 10, 100), -- Junior Developer
(189, 9, 100),  -- Senior Developer
(190, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(191, 20, 60),  -- Digital Marketing Specialist (60%)
(191, 23, 40),  -- Social Media Manager (40%)

(192, 10, 100), -- Junior Developer
(193, 9, 100),  -- Senior Developer
(194, 11, 100), -- QA Engineer
(195, 28, 100), -- Accountant

-- Employee with multiple positions
(196, 26, 70),  -- HR Assistant (70%)
(196, 25, 30),  -- Recruitment Specialist (30%)

(197, 10, 100), -- Junior Developer
(198, 14, 100), -- Data Analyst
(199, 9, 100),  -- Senior Developer
(200, 35, 100), -- Customer Support Specialist

-- Continue with employees 201-300
(201, 9, 100),  -- Senior Developer
(202, 17, 100), -- Junior Designer
(203, 10, 100), -- Junior Developer
(204, 35, 100), -- Customer Support Specialist
(205, 13, 100), -- Data Scientist

-- Employee with multiple positions
(206, 28, 75),  -- Accountant (75%)
(206, 29, 25),  -- Financial Analyst (25%)

(207, 9, 100),  -- Senior Developer
(208, 31, 100), -- Sales Representative
(209, 10, 100), -- Junior Developer
(210, 21, 100), -- Content Creator

-- Employee with multiple positions
(211, 16, 60),  -- Senior Designer (60%)
(211, 15, 40),  -- UX/UI Design Lead (40%)

(212, 35, 100), -- Customer Support Specialist
(213, 9, 100),  -- Senior Developer
(214, 14, 100), -- Data Analyst
(215, 10, 100), -- Junior Developer

-- Employee with triple position (rare)
(216, 33, 40),  -- IT Support Specialist (40%)
(216, 10, 40),  -- Junior Developer (40%)
(216, 11, 20),  -- QA Engineer (20%)

(217, 9, 100),  -- Senior Developer
(218, 35, 100), -- Customer Support Specialist
(219, 28, 100), -- Accountant
(220, 17, 100), -- Junior Designer

-- Employee with multiple positions
(221, 31, 80),  -- Sales Representative (80%)
(221, 30, 20),  -- Sales Manager (20%)

(222, 10, 100), -- Junior Developer
(223, 9, 100),  -- Senior Developer
(224, 20, 100), -- Digital Marketing Specialist
(225, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(226, 13, 60),  -- Data Scientist (60%)
(226, 14, 40),  -- Data Analyst (40%)

(227, 9, 100),  -- Senior Developer
(228, 18, 100), -- Graphic Designer
(229, 10, 100), -- Junior Developer
(230, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(231, 22, 70),  -- SEO Specialist (70%)
(231, 23, 30),  -- Social Media Manager (30%)

(232, 28, 100), -- Accountant
(233, 9, 100),  -- Senior Developer
(234, 31, 100), -- Sales Representative
(235, 10, 100), -- Junior Developer

-- Employee with multiple positions
(236, 35, 75),  -- Customer Support Specialist (75%)
(236, 34, 25),  -- Customer Support Manager (25%)

(237, 11, 100), -- QA Engineer
(238, 9, 100),  -- Senior Developer
(239, 17, 100), -- Junior Designer
(240, 10, 100), -- Junior Developer

-- Employee with multiple positions
(241, 33, 70),  -- IT Support Specialist (70%)
(241, 32, 30),  -- IT Support Manager (30%)

(242, 35, 100), -- Customer Support Specialist
(243, 9, 100),  -- Senior Developer
(244, 14, 100), -- Data Analyst
(245, 28, 100), -- Accountant

-- Employee with multiple positions
(246, 10, 60),  -- Junior Developer (60%)
(246, 11, 40),  -- QA Engineer (40%)

(247, 9, 100),  -- Senior Developer
(248, 21, 100), -- Content Creator
(249, 31, 100), -- Sales Representative
(250, 10, 100), -- Junior Developer

-- Employee with multiple positions
(251, 13, 80),  -- Data Scientist (80%)
(251, 12, 20),  -- Data Science Manager (20%)

(252, 35, 100), -- Customer Support Specialist
(253, 9, 100),  -- Senior Developer
(254, 17, 100), -- Junior Designer
(255, 28, 100), -- Accountant

-- Employee with multiple positions
(256, 20, 65),  -- Digital Marketing Specialist (65%)
(256, 21, 35),  -- Content Creator (35%)

(257, 10, 100), -- Junior Developer
(258, 9, 100),  -- Senior Developer
(259, 14, 100), -- Data Analyst
(260, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(261, 31, 70),  -- Sales Representative (70%)
(261, 30, 30),  -- Sales Manager (30%)

(262, 10, 100), -- Junior Developer
(263, 9, 100),  -- Senior Developer
(264, 25, 100), -- Recruitment Specialist
(265, 28, 100), -- Accountant

-- Employee with multiple positions
(266, 17, 60),  -- Junior Designer (60%)
(266, 16, 40),  -- Senior Designer (40%)

(267, 35, 100), -- Customer Support Specialist
(268, 10, 100), -- Junior Developer
(269, 9, 100),  -- Senior Developer
(270, 31, 100), -- Sales Representative

-- Employee with multiple positions
(271, 11, 75),  -- QA Engineer (75%)
(271, 10, 25),  -- Junior Developer (25%)

(272, 13, 100), -- Data Scientist
(273, 35, 100), -- Customer Support Specialist
(274, 9, 100),  -- Senior Developer
(275, 28, 100), -- Accountant

-- Employee with multiple positions
(276, 33, 65),  -- IT Support Specialist (65%)
(276, 10, 35),  -- Junior Developer (35%)

(277, 21, 100), -- Content Creator
(278, 9, 100),  -- Senior Developer
(279, 16, 100), -- Senior Designer
(280, 10, 100), -- Junior Developer

-- Employee with multiple positions
(281, 31, 80),  -- Sales Representative (80%)
(281, 30, 20),  -- Sales Manager (20%)

(282, 35, 100), -- Customer Support Specialist
(283, 9, 100),  -- Senior Developer
(284, 14, 100), -- Data Analyst
(285, 10, 100), -- Junior Developer

-- Employee with multiple positions
(286, 18, 70),  -- Graphic Designer (70%)
(286, 17, 30),  -- Junior Designer (30%)

(287, 28, 100), -- Accountant
(288, 9, 100),  -- Senior Developer
(289, 35, 100), -- Customer Support Specialist
(290, 10, 100), -- Junior Developer

-- Employee with multiple positions
(291, 13, 60),  -- Data Scientist (60%)
(291, 14, 40),  -- Data Analyst (40%)

(292, 20, 100), -- Digital Marketing Specialist
(293, 9, 100),  -- Senior Developer
(294, 31, 100), -- Sales Representative
(295, 28, 100), -- Accountant

-- Employee with multiple positions
(296, 10, 65),  -- Junior Developer (65%)
(296, 11, 35),  -- QA Engineer (35%)

(297, 9, 100),  -- Senior Developer
(298, 35, 100), -- Customer Support Specialist
(299, 22, 100), -- SEO Specialist
(300, 17, 100), -- Junior Designer

-- Continue with employees 301-400
(301, 9, 100),  -- Senior Developer
(302, 21, 100), -- Content Creator
(303, 10, 100), -- Junior Developer
(304, 35, 100), -- Customer Support Specialist
(305, 14, 100), -- Data Analyst

-- Employee with multiple positions
(306, 28, 75),  -- Accountant (75%)
(306, 29, 25),  -- Financial Analyst (25%)

(307, 9, 100),  -- Senior Developer
(308, 16, 100), -- Senior Designer
(309, 10, 100), -- Junior Developer
(310, 31, 100), -- Sales Representative

-- Employee with multiple positions
(311, 33, 60),  -- IT Support Specialist (60%)
(311, 10, 40),  -- Junior Developer (40%)

(312, 35, 100), -- Customer Support Specialist
(313, 9, 100),  -- Senior Developer
(314, 28, 100), -- Accountant
(315, 10, 100), -- Junior Developer

-- Employee with multiple positions
(316, 17, 70),  -- Junior Designer (70%)
(316, 18, 30),  -- Graphic Designer (30%)

(317, 9, 100),  -- Senior Developer
(318, 35, 100), -- Customer Support Specialist
(319, 13, 100), -- Data Scientist
(320, 31, 100), -- Sales Representative

-- Employee with triple position (rare)
(321, 10, 40),  -- Junior Developer (40%)
(321, 11, 30),  -- QA Engineer (30%)
(321, 33, 30),  -- IT Support Specialist (30%)

(322, 9, 100),  -- Senior Developer
(323, 28, 100), -- Accountant
(324, 20, 100), -- Digital Marketing Specialist
(325, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(326, 26, 60),  -- HR Assistant (60%)
(326, 25, 40),  -- Recruitment Specialist (40%)

(327, 9, 100),  -- Senior Developer
(328, 14, 100), -- Data Analyst
(329, 10, 100), -- Junior Developer
(330, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(331, 22, 70),  -- SEO Specialist (70%)
(331, 21, 30),  -- Content Creator (30%)

(332, 9, 100),  -- Senior Developer
(333, 31, 100), -- Sales Representative
(334, 28, 100), -- Accountant
(335, 10, 100), -- Junior Developer

-- Employee with multiple positions
(336, 33, 80),  -- IT Support Specialist (80%)
(336, 11, 20),  -- QA Engineer (20%)

(337, 35, 100), -- Customer Support Specialist
(338, 9, 100),  -- Senior Developer
(339, 17, 100), -- Junior Designer
(340, 10, 100), -- Junior Developer

-- Employee with multiple positions
(341, 13, 60),  -- Data Scientist (60%)
(341, 14, 40),  -- Data Analyst (40%)

(342, 35, 100), -- Customer Support Specialist
(343, 9, 100),  -- Senior Developer
(344, 28, 100), -- Accountant
(345, 31, 100), -- Sales Representative

-- Employee with multiple positions
(346, 10, 70),  -- Junior Developer (70%)
(346, 11, 30),  -- QA Engineer (30%)

(347, 9, 100),  -- Senior Developer
(348, 35, 100), -- Customer Support Specialist
(349, 21, 100), -- Content Creator
(350, 16, 100), -- Senior Designer

-- Employee with multiple positions
(351, 20, 65),  -- Digital Marketing Specialist (65%)
(351, 22, 35),  -- SEO Specialist (35%)

(352, 10, 100), -- Junior Developer
(353, 9, 100),  -- Senior Developer
(354, 35, 100), -- Customer Support Specialist
(355, 28, 100), -- Accountant

-- Employee with multiple positions
(356, 33, 75),  -- IT Support Specialist (75%)
(356, 32, 25),  -- IT Support Manager (25%)

(357, 9, 100),  -- Senior Developer
(358, 14, 100), -- Data Analyst
(359, 10, 100), -- Junior Developer
(360, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(361, 31, 70),  -- Sales Representative (70%)
(361, 30, 30),  -- Sales Manager (30%)

(362, 9, 100),  -- Senior Developer
(363, 17, 100), -- Junior Designer
(364, 28, 100), -- Accountant
(365, 10, 100), -- Junior Developer

-- Employee with multiple positions
(366, 18, 60),  -- Graphic Designer (60%)
(366, 17, 40),  -- Junior Designer (40%)

(367, 9, 100),  -- Senior Developer
(368, 35, 100), -- Customer Support Specialist
(369, 13, 100), -- Data Scientist
(370, 31, 100), -- Sales Representative

-- Employee with multiple positions
(371, 10, 65),  -- Junior Developer (65%)
(371, 11, 35),  -- QA Engineer (35%)

(372, 9, 100),  -- Senior Developer
(373, 28, 100), -- Accountant
(374, 35, 100), -- Customer Support Specialist
(375, 21, 100), -- Content Creator

-- Employee with multiple positions
(376, 20, 70),  -- Digital Marketing Specialist (70%)
(376, 23, 30),  -- Social Media Manager (30%)

(377, 10, 100), -- Junior Developer
(378, 9, 100),  -- Senior Developer
(379, 35, 100), -- Customer Support Specialist
(380, 14, 100), -- Data Analyst

-- Employee with multiple positions
(381, 33, 75),  -- IT Support Specialist (75%) 
(381, 11, 25),  -- QA Engineer (25%)

(382, 10, 100), -- Junior Developer
(383, 9, 100),  -- Senior Developer
(384, 28, 100), -- Accountant
(385, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(386, 17, 80),  -- Junior Designer (80%)
(386, 18, 20),  -- Graphic Designer (20%)

(387, 9, 100),  -- Senior Developer
(388, 31, 100), -- Sales Representative
(389, 10, 100), -- Junior Developer
(390, 13, 100), -- Data Scientist

-- Employee with multiple positions
(391, 26, 65),  -- HR Assistant (65%)
(391, 25, 35),  -- Recruitment Specialist (35%)

(392, 35, 100), -- Customer Support Specialist
(393, 9, 100),  -- Senior Developer
(394, 14, 100), -- Data Analyst
(395, 28, 100), -- Accountant

-- Employee with multiple positions
(396, 10, 70),  -- Junior Developer (70%)
(396, 11, 30),  -- QA Engineer (30%)

(397, 9, 100),  -- Senior Developer
(398, 21, 100), -- Content Creator
(399, 35, 100), -- Customer Support Specialist
(400, 16, 100), -- Senior Designer

-- Continuing with employees 401-500
(401, 9, 100),  -- Senior Developer
(402, 35, 100), -- Customer Support Specialist
(403, 10, 100), -- Junior Developer
(404, 28, 100), -- Accountant
(405, 14, 100), -- Data Analyst

-- Employee with multiple positions
(406, 31, 75),  -- Sales Representative (75%)
(406, 30, 25),  -- Sales Manager (25%)

(407, 9, 100),  -- Senior Developer
(408, 17, 100), -- Junior Designer
(409, 10, 100), -- Junior Developer
(410, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(411, 13, 60),  -- Data Scientist (60%)
(411, 12, 40),  -- Data Science Manager (40%)

(412, 28, 100), -- Accountant
(413, 9, 100),  -- Senior Developer
(414, 31, 100), -- Sales Representative
(415, 10, 100), -- Junior Developer

-- Employee with multiple positions
(416, 33, 70),  -- IT Support Specialist (70%)
(416, 11, 30),  -- QA Engineer (30%)

(417, 9, 100),  -- Senior Developer
(418, 35, 100), -- Customer Support Specialist
(419, 18, 100), -- Graphic Designer
(420, 21, 100), -- Content Creator

-- Employee with multiple positions
(421, 20, 65),  -- Digital Marketing Specialist (65%)
(421, 23, 35),  -- Social Media Manager (35%)

(422, 9, 100),  -- Senior Developer
(423, 14, 100), -- Data Analyst
(424, 35, 100), -- Customer Support Specialist
(425, 28, 100), -- Accountant

-- Employee with triple position (rare)
(426, 10, 40),  -- Junior Developer (40%)
(426, 11, 30),  -- QA Engineer (30%)
(426, 33, 30),  -- IT Support Specialist (30%)

(427, 9, 100),  -- Senior Developer
(428, 26, 100), -- HR Assistant
(429, 31, 100), -- Sales Representative
(430, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(431, 16, 80),  -- Senior Designer (80%)
(431, 15, 20),  -- UX/UI Design Lead (20%)

(432, 10, 100), -- Junior Developer
(433, 9, 100),  -- Senior Developer
(434, 35, 100), -- Customer Support Specialist
(435, 28, 100), -- Accountant

-- Employee with multiple positions
(436, 22, 70),  -- SEO Specialist (70%)
(436, 21, 30),  -- Content Creator (30%)

(437, 9, 100),  -- Senior Developer
(438, 14, 100), -- Data Analyst
(439, 10, 100), -- Junior Developer
(440, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(441, 31, 75),  -- Sales Representative (75%)
(441, 30, 25),  -- Sales Manager (25%)

(442, 9, 100),  -- Senior Developer
(443, 17, 100), -- Junior Designer
(444, 28, 100), -- Accountant
(445, 10, 100), -- Junior Developer

-- Employee with multiple positions
(446, 13, 60),  -- Data Scientist (60%)
(446, 14, 40),  -- Data Analyst (40%)

(447, 9, 100),  -- Senior Developer
(448, 35, 100), -- Customer Support Specialist
(449, 21, 100), -- Content Creator
(450, 31, 100), -- Sales Representative

-- Employee with multiple positions
(451, 33, 80),  -- IT Support Specialist (80%)
(451, 32, 20),  -- IT Support Manager (20%)

(452, 10, 100), -- Junior Developer
(453, 9, 100),  -- Senior Developer
(454, 28, 100), -- Accountant
(455, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(456, 18, 75),  -- Graphic Designer (75%)
(456, 17, 25),  -- Junior Designer (25%)

(457, 9, 100),  -- Senior Developer
(458, 14, 100), -- Data Analyst
(459, 10, 100), -- Junior Developer
(460, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(461, 20, 70),  -- Digital Marketing Specialist (70%)
(461, 22, 30),  -- SEO Specialist (30%)

(462, 9, 100),  -- Senior Developer
(463, 31, 100), -- Sales Representative
(464, 28, 100), -- Accountant
(465, 10, 100), -- Junior Developer

-- Employee with multiple positions
(466, 26, 65),  -- HR Assistant (65%)
(466, 25, 35),  -- Recruitment Specialist (35%)

(467, 9, 100),  -- Senior Developer
(468, 35, 100), -- Customer Support Specialist
(469, 16, 100), -- Senior Designer
(470, 14, 100), -- Data Analyst

-- Employee with multiple positions
(471, 13, 75),  -- Data Scientist (75%)
(471, 12, 25),  -- Data Science Manager (25%)

(472, 10, 100), -- Junior Developer
(473, 9, 100),  -- Senior Developer
(474, 28, 100), -- Accountant
(475, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(476, 11, 70),  -- QA Engineer (70%)
(476, 10, 30),  -- Junior Developer (30%)

(477, 9, 100),  -- Senior Developer
(478, 17, 100), -- Junior Designer
(479, 31, 100), -- Sales Representative
(480, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(481, 33, 60),  -- IT Support Specialist (60%)
(481, 10, 40),  -- Junior Developer (40%)

(482, 9, 100),  -- Senior Developer
(483, 14, 100), -- Data Analyst
(484, 28, 100), -- Accountant
(485, 21, 100), -- Content Creator

-- Employee with multiple positions
(486, 20, 75),  -- Digital Marketing Specialist (75%)
(486, 23, 25),  -- Social Media Manager (25%)

(487, 9, 100),  -- Senior Developer
(488, 35, 100), -- Customer Support Specialist
(489, 10, 100), -- Junior Developer
(490, 28, 100), -- Accountant

-- Employee with multiple positions
(491, 31, 80),  -- Sales Representative (80%)
(491, 30, 20),  -- Sales Manager (20%)

(492, 9, 100),  -- Senior Developer
(493, 16, 100), -- Senior Designer
(494, 35, 100), -- Customer Support Specialist
(495, 10, 100), -- Junior Developer

-- Employee with multiple positions
(496, 13, 65),  -- Data Scientist (65%)
(496, 14, 35),  -- Data Analyst (35%)

(497, 9, 100),  -- Senior Developer
(498, 28, 100), -- Accountant
(499, 10, 100), -- Junior Developer
(500, 35, 100),  -- Customer Support Specialist

-- Employee with multiple positions
(501, 18, 70),  -- Graphic Designer (70%)
(501, 21, 30),  -- Content Creator (30%)

(502, 9, 100),  -- Senior Developer
(503, 35, 100), -- Customer Support Specialist
(504, 10, 100), -- Junior Developer
(505, 31, 100), -- Sales Representative

-- Employee with multiple positions
(506, 26, 75),  -- HR Assistant (75%)
(506, 27, 25),  -- HR Coordinator (25%)

(507, 9, 100),  -- Senior Developer
(508, 14, 100), -- Data Analyst
(509, 28, 100), -- Accountant
(510, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(511, 11, 60),  -- QA Engineer (60%)
(511, 12, 40),  -- Data Science Manager (40%)

(512, 9, 100),  -- Senior Developer
(513, 16, 100), -- Senior Designer
(514, 10, 100), -- Junior Developer
(515, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(516, 20, 80),  -- Digital Marketing Specialist (80%)
(516, 21, 20),  -- Content Creator (20%)

(517, 9, 100),  -- Senior Developer
(518, 31, 100), -- Sales Representative
(519, 28, 100), -- Accountant
(520, 10, 100), -- Junior Developer

-- Employee with multiple positions
(521, 33, 70),  -- IT Support Specialist (70%)
(521, 34, 30),  -- Network Administrator (30%)

(522, 9, 100),  -- Senior Developer
(523, 35, 100), -- Customer Support Specialist
(524, 17, 100), -- Junior Designer
(525, 14, 100), -- Data Analyst

-- Employee with multiple positions
(526, 13, 65),  -- Data Scientist (65%)
(526, 15, 35),  -- Business Intelligence Analyst (35%)

(527, 10, 100), -- Junior Developer
(528, 9, 100),  -- Senior Developer
(529, 28, 100), -- Accountant
(530, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(531, 18, 75),  -- Graphic Designer (75%)
(531, 19, 25),  -- UI/UX Designer (25%)

(532, 9, 100),  -- Senior Developer
(533, 21, 100), -- Content Creator
(534, 31, 100), -- Sales Representative
(535, 10, 100), -- Junior Developer

-- Employee with multiple positions
(536, 20, 60),  -- Digital Marketing Specialist (60%)
(536, 22, 40),  -- SEO Specialist (40%)

(537, 9, 100),  -- Senior Developer
(538, 14, 100), -- Data Analyst
(539, 28, 100), -- Accountant
(540, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(541, 26, 70),  -- HR Assistant (70%)
(541, 25, 30),  -- Recruitment Specialist (30%)

(542, 9, 100),  -- Senior Developer
(543, 10, 100), -- Junior Developer
(544, 16, 100), -- Senior Designer
(545, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(546, 11, 75),  -- QA Engineer (75%)
(546, 8, 25),   -- Technical Lead (25%)

(547, 9, 100),  -- Senior Developer
(548, 31, 100), -- Sales Representative
(549, 28, 100), -- Accountant
(550, 10, 100), -- Junior Developer

-- Employee with multiple positions
(551, 13, 80),  -- Data Scientist (80%)
(551, 14, 20),  -- Data Analyst (20%)

(552, 9, 100),  -- Senior Developer
(553, 35, 100), -- Customer Support Specialist
(554, 21, 100), -- Content Creator
(555, 17, 100), -- Junior Designer

-- Employee with multiple positions
(556, 33, 65),  -- IT Support Specialist (65%)
(556, 32, 35),  -- IT Support Manager (35%)

(557, 9, 100),  -- Senior Developer
(558, 14, 100), -- Data Analyst
(559, 28, 100), -- Accountant
(560, 10, 100), -- Junior Developer

-- Employee with multiple positions
(561, 20, 70),  -- Digital Marketing Specialist (70%)
(561, 23, 30),  -- Social Media Manager (30%)

(562, 9, 100),  -- Senior Developer
(563, 35, 100), -- Customer Support Specialist
(564, 10, 100), -- Junior Developer
(565, 31, 100), -- Sales Representative

-- Employee with multiple positions
(566, 18, 60),  -- Graphic Designer (60%)
(566, 16, 40),  -- Senior Designer (40%)

(567, 9, 100),  -- Senior Developer
(568, 28, 100), -- Accountant
(569, 35, 100), -- Customer Support Specialist
(570, 14, 100), -- Data Analyst

-- Employee with multiple positions
(571, 11, 65),  -- QA Engineer (65%)
(571, 10, 35),  -- Junior Developer (35%)

(572, 9, 100),  -- Senior Developer
(573, 21, 100), -- Content Creator
(574, 10, 100), -- Junior Developer
(575, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(576, 26, 75),  -- HR Assistant (75%)
(576, 24, 25),  -- HR Manager (25%)

(577, 9, 100),  -- Senior Developer
(578, 31, 100), -- Sales Representative
(579, 28, 100), -- Accountant
(580, 10, 100), -- Junior Developer

-- Employee with multiple positions
(581, 13, 70),  -- Data Scientist (70%)
(581, 12, 30),  -- Data Science Manager (30%)

(582, 9, 100),  -- Senior Developer
(583, 35, 100), -- Customer Support Specialist
(584, 17, 100), -- Junior Designer
(585, 14, 100), -- Data Analyst

-- Employee with multiple positions
(586, 20, 80),  -- Digital Marketing Specialist (80%)
(586, 22, 20),  -- SEO Specialist (20%)

(587, 10, 100), -- Junior Developer
(588, 9, 100),  -- Senior Developer
(589, 28, 100), -- Accountant
(590, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(591, 33, 75),  -- IT Support Specialist (75%)
(591, 34, 25),  -- Network Administrator (25%)

(592, 9, 100),  -- Senior Developer
(593, 16, 100), -- Senior Designer
(594, 31, 100), -- Sales Representative
(595, 10, 100), -- Junior Developer

-- Employee with multiple positions
(596, 18, 65),  -- Graphic Designer (65%)
(596, 19, 35),  -- UI/UX Designer (35%)

(597, 9, 100),  -- Senior Developer
(598, 14, 100), -- Data Analyst
(599, 28, 100), -- Accountant
(600, 35, 100), -- Customer Support Specialist

-- Continuing with more employees...

-- Employee with multiple positions
(601, 11, 70),  -- QA Engineer (70%)
(601, 9, 30),   -- Senior Developer (30%)

(602, 10, 100), -- Junior Developer
(603, 21, 100), -- Content Creator
(604, 31, 100), -- Sales Representative
(605, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(606, 26, 60),  -- HR Assistant (60%)
(606, 25, 40),  -- Recruitment Specialist (40%)

(607, 9, 100),  -- Senior Developer
(608, 14, 100), -- Data Analyst
(609, 28, 100), -- Accountant
(610, 10, 100), -- Junior Developer

-- Employee with multiple positions
(611, 13, 75),  -- Data Scientist (75%)
(611, 15, 25),  -- Business Intelligence Analyst (25%)

(612, 9, 100),  -- Senior Developer
(613, 35, 100), -- Customer Support Specialist
(614, 17, 100), -- Junior Designer
(615, 31, 100), -- Sales Representative

-- Employee with multiple positions
(616, 20, 70),  -- Digital Marketing Specialist (70%)
(616, 21, 30),  -- Content Creator (30%)

(617, 9, 100),  -- Senior Developer
(618, 28, 100), -- Accountant
(619, 10, 100), -- Junior Developer
(620, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(621, 33, 65),  -- IT Support Specialist (65%)
(621, 10, 35),  -- Junior Developer (35%)

(622, 9, 100),  -- Senior Developer
(623, 16, 100), -- Senior Designer
(624, 14, 100), -- Data Analyst
(625, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(626, 18, 80),  -- Graphic Designer (80%)
(626, 17, 20),  -- Junior Designer (20%)

(627, 9, 100),  -- Senior Developer
(628, 31, 100), -- Sales Representative
(629, 28, 100), -- Accountant
(630, 10, 100), -- Junior Developer

-- Employee with multiple positions
(631, 11, 75),  -- QA Engineer (75%)
(631, 8, 25),   -- Technical Lead (25%)

(632, 9, 100),  -- Senior Developer
(633, 35, 100), -- Customer Support Specialist
(634, 21, 100), -- Content Creator
(635, 14, 100), -- Data Analyst

-- Employee with multiple positions
(636, 26, 70),  -- HR Assistant (70%)
(636, 27, 30),  -- HR Coordinator (30%)

(637, 10, 100), -- Junior Developer
(638, 9, 100),  -- Senior Developer
(639, 28, 100), -- Accountant
(640, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(641, 13, 60),  -- Data Scientist (60%)
(641, 14, 40),  -- Data Analyst (40%)

(642, 9, 100),  -- Senior Developer
(643, 17, 100), -- Junior Designer
(644, 31, 100), -- Sales Representative 
(645, 10, 100), -- Junior Developer

-- Employee with multiple positions
(646, 20, 75),  -- Digital Marketing Specialist (75%)
(646, 22, 25),  -- SEO Specialist (25%)

(647, 9, 100),  -- Senior Developer
(648, 14, 100), -- Data Analyst
(649, 28, 100), -- Accountant
(650, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(651, 33, 70),  -- IT Support Specialist (70%)
(651, 32, 30),  -- IT Support Manager (30%)

(652, 9, 100),  -- Senior Developer
(653, 10, 100), -- Junior Developer
(654, 16, 100), -- Senior Designer
(655, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(656, 18, 65),  -- Graphic Designer (65%)
(656, 19, 35),  -- UI/UX Designer (35%)

(657, 9, 100),  -- Senior Developer
(658, 31, 100), -- Sales Representative
(659, 28, 100), -- Accountant
(660, 10, 100), -- Junior Developer

-- Employee with multiple positions
(661, 11, 80),  -- QA Engineer (80%)
(661, 10, 20),  -- Junior Developer (20%)

(662, 9, 100),  -- Senior Developer
(663, 35, 100), -- Customer Support Specialist
(664, 21, 100), -- Content Creator
(665, 14, 100), -- Data Analyst

-- Employee with multiple positions
(666, 26, 75),  -- HR Assistant (75%)
(666, 25, 25),  -- Recruitment Specialist (25%)

(667, 9, 100),  -- Senior Developer
(668, 28, 100), -- Accountant
(669, 10, 100), -- Junior Developer
(670, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(671, 13, 70),  -- Data Scientist (70%)
(671, 15, 30),  -- Business Intelligence Analyst (30%)

(672, 9, 100),  -- Senior Developer
(673, 17, 100), -- Junior Designer
(674, 31, 100), -- Sales Representative
(675, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(676, 20, 60),  -- Digital Marketing Specialist (60%)
(676, 23, 40),  -- Social Media Manager (40%)

(677, 10, 100), -- Junior Developer
(678, 9, 100),  -- Senior Developer
(679, 28, 100), -- Accountant
(680, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(681, 33, 75),  -- IT Support Specialist (75%)
(681, 34, 25),  -- Network Administrator (25%)

(682, 9, 100),  -- Senior Developer
(683, 16, 100), -- Senior Designer
(684, 14, 100), -- Data Analyst
(685, 10, 100), -- Junior Developer

-- Employee with multiple positions
(686, 18, 80),  -- Graphic Designer (80%)
(686, 21, 20),  -- Content Creator (20%)

(687, 9, 100),  -- Senior Developer
(688, 31, 100), -- Sales Representative
(689, 28, 100), -- Accountant
(690, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(691, 11, 65),  -- QA Engineer (65%)
(691, 9, 35),   -- Senior Developer (35%)

(692, 10, 100), -- Junior Developer
(693, 35, 100), -- Customer Support Specialist
(694, 21, 100), -- Content Creator
(695, 14, 100), -- Data Analyst

-- Employee with multiple positions
(696, 26, 70),  -- HR Assistant (70%)
(696, 24, 30),  -- HR Manager (30%)

(697, 9, 100),  -- Senior Developer
(698, 28, 100), -- Accountant
(699, 10, 100), -- Junior Developer
(700, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(701, 13, 60),  -- Data Scientist (60%)
(701, 14, 40),  -- Data Analyst (40%)

(702, 9, 100),  -- Senior Developer
(703, 10, 100), -- Junior Developer
(704, 28, 100), -- Accountant
(705, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(706, 20, 75),  -- Digital Marketing Specialist (75%)
(706, 22, 25),  -- SEO Specialist (25%)

(707, 9, 100),  -- Senior Developer
(708, 14, 100), -- Data Analyst
(709, 28, 100), -- Accountant
(710, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(711, 33, 70),  -- IT Support Specialist (70%)
(711, 32, 30),  -- IT Support Manager (30%)

(712, 9, 100),  -- Senior Developer
(713, 10, 100), -- Junior Developer
(714, 16, 100), -- Senior Designer
(715, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(716, 18, 65),  -- Graphic Designer (65%)
(716, 19, 35),  -- UI/UX Designer (35%)

(717, 9, 100),  -- Senior Developer
(718, 31, 100), -- Sales Representative
(719, 28, 100), -- Accountant
(720, 10, 100), -- Junior Developer

-- Employee with multiple positions
(721, 11, 80),  -- QA Engineer (80%)
(721, 10, 20),  -- Junior Developer (20%)

(722, 9, 100),  -- Senior Developer
(723, 35, 100), -- Customer Support Specialist
(724, 21, 100), -- Content Creator
(725, 14, 100), -- Data Analyst

-- Employee with multiple positions
(726, 26, 75),  -- HR Assistant (75%)
(726, 25, 25),  -- Recruitment Specialist (25%)

(727, 9, 100),  -- Senior Developer
(728, 28, 100), -- Accountant
(729, 10, 100), -- Junior Developer
(730, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(731, 13, 70),  -- Data Scientist (70%)
(731, 15, 30),  -- Business Intelligence Analyst (30%)

(732, 9, 100),  -- Senior Developer
(733, 17, 100), -- Junior Designer
(734, 31, 100), -- Sales Representative
(735, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(736, 20, 60),  -- Digital Marketing Specialist (60%)
(736, 23, 40),  -- Social Media Manager (40%)

(737, 10, 100), -- Junior Developer
(738, 9, 100),  -- Senior Developer
(739, 28, 100), -- Accountant
(740, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(741, 33, 75),  -- IT Support Specialist (75%)
(741, 34, 25),  -- Network Administrator (25%)

(742, 9, 100),  -- Senior Developer
(743, 16, 100), -- Senior Designer
(744, 14, 100), -- Data Analyst
(745, 10, 100), -- Junior Developer

-- Employee with multiple positions
(746, 18, 80),  -- Graphic Designer (80%)
(746, 21, 20),  -- Content Creator (20%)

(747, 9, 100),  -- Senior Developer
(748, 31, 100), -- Sales Representative
(749, 28, 100), -- Accountant
(750, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(751, 11, 65),  -- QA Engineer (65%)
(751, 9, 35),   -- Senior Developer (35%)

(752, 10, 100), -- Junior Developer
(753, 35, 100), -- Customer Support Specialist
(754, 21, 100), -- Content Creator
(755, 14, 100), -- Data Analyst

-- Employee with multiple positions
(756, 26, 70),  -- HR Assistant (70%)
(756, 24, 30),  -- HR Manager (30%)

(757, 9, 100),  -- Senior Developer
(758, 28, 100), -- Accountant
(759, 10, 100), -- Junior Developer
(760, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(761, 13, 60),  -- Data Scientist (60%)
(761, 14, 40),  -- Data Analyst (40%)

(762, 9, 100),  -- Senior Developer
(763, 10, 100), -- Junior Developer
(764, 28, 100), -- Accountant
(765, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(766, 20, 75),  -- Digital Marketing Specialist (75%)
(766, 22, 25),  -- SEO Specialist (25%)

(767, 9, 100),  -- Senior Developer
(768, 14, 100), -- Data Analyst
(769, 28, 100), -- Accountant
(770, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(771, 33, 70),  -- IT Support Specialist (70%)
(771, 32, 30),  -- IT Support Manager (30%)

(772, 9, 100),  -- Senior Developer
(773, 10, 100), -- Junior Developer
(774, 16, 100), -- Senior Designer
(775, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(776, 18, 65),  -- Graphic Designer (65%)
(776, 19, 35),  -- UI/UX Designer (35%)

(777, 9, 100),  -- Senior Developer
(778, 31, 100), -- Sales Representative
(779, 28, 100), -- Accountant
(780, 10, 100), -- Junior Developer

-- Employee with multiple positions
(781, 11, 80),  -- QA Engineer (80%)
(781, 10, 20),  -- Junior Developer (20%)

(782, 9, 100),  -- Senior Developer
(783, 35, 100), -- Customer Support Specialist
(784, 21, 100), -- Content Creator
(785, 14, 100), -- Data Analyst

-- Employee with multiple positions
(786, 26, 75),  -- HR Assistant (75%)
(786, 25, 25),  -- Recruitment Specialist (25%)

(787, 9, 100),  -- Senior Developer
(788, 28, 100), -- Accountant
(789, 10, 100), -- Junior Developer
(790, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(791, 13, 60),  -- Data Scientist (60%)
(791, 14, 40),  -- Data Analyst (40%)

(792, 9, 100),  -- Senior Developer
(793, 10, 100), -- Junior Developer
(794, 28, 100), -- Accountant
(795, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(796, 20, 75),  -- Digital Marketing Specialist (75%)
(796, 22, 25),  -- SEO Specialist (25%)

(797, 9, 100),  -- Senior Developer
(798, 14, 100), -- Data Analyst
(799, 28, 100), -- Accountant
(800, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(801, 33, 70),  -- IT Support Specialist (70%)
(801, 32, 30),  -- IT Support Manager (30%)

(802, 9, 100),  -- Senior Developer
(803, 10, 100), -- Junior Developer
(804, 16, 100), -- Senior Designer
(805, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(806, 18, 65),  -- Graphic Designer (65%)
(806, 19, 35),  -- UI/UX Designer (35%)

(807, 9, 100),  -- Senior Developer
(808, 31, 100), -- Sales Representative
(809, 28, 100), -- Accountant
(810, 10, 100), -- Junior Developer

-- Employee with multiple positions
(811, 11, 80),  -- QA Engineer (80%)
(811, 10, 20),  -- Junior Developer (20%)

(812, 9, 100),  -- Senior Developer
(813, 35, 100), -- Customer Support Specialist
(814, 21, 100), -- Content Creator
(815, 14, 100), -- Data Analyst

-- Employee with multiple positions
(816, 26, 75),  -- HR Assistant (75%)
(816, 25, 25),  -- Recruitment Specialist (25%)

(817, 9, 100),  -- Senior Developer
(818, 28, 100), -- Accountant
(819, 10, 100), -- Junior Developer
(820, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(821, 13, 70),  -- Data Scientist (70%)
(821, 15, 30),  -- Business Intelligence Analyst (30%)

(822, 9, 100),  -- Senior Developer
(823, 17, 100), -- Junior Designer
(824, 31, 100), -- Sales Representative
(825, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(826, 20, 60),  -- Digital Marketing Specialist (60%)
(826, 23, 40),  -- Social Media Manager (40%)

(827, 10, 100), -- Junior Developer
(828, 9, 100),  -- Senior Developer
(829, 28, 100), -- Accountant
(830, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(831, 33, 75),  -- IT Support Specialist (75%)
(831, 34, 25),  -- Network Administrator (25%)

(832, 9, 100),  -- Senior Developer
(833, 16, 100), -- Senior Designer
(834, 14, 100), -- Data Analyst
(835, 10, 100), -- Junior Developer

-- Employee with multiple positions
(836, 18, 80),  -- Graphic Designer (80%)
(836, 21, 20),  -- Content Creator (20%)

(837, 9, 100),  -- Senior Developer
(838, 31, 100), -- Sales Representative
(839, 28, 100), -- Accountant
(840, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(841, 11, 65),  -- QA Engineer (65%)
(841, 9, 35),   -- Senior Developer (35%)

(842, 10, 100), -- Junior Developer
(843, 35, 100), -- Customer Support Specialist
(844, 21, 100), -- Content Creator
(845, 14, 100), -- Data Analyst

-- Employee with multiple positions
(846, 26, 70),  -- HR Assistant (70%)
(846, 24, 30),  -- HR Manager (30%)

(847, 9, 100),  -- Senior Developer
(848, 28, 100), -- Accountant
(849, 10, 100), -- Junior Developer
(850, 35, 100), -- Customer Support Specialist
-- Employee with multiple positions
(851, 13, 60),  -- Data Scientist (60%)
(851, 14, 40),  -- Data Analyst (40%)

(852, 9, 100),  -- Senior Developer
(853, 10, 100), -- Junior Developer
(854, 28, 100), -- Accountant
(855, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(856, 20, 75),  -- Digital Marketing Specialist (75%)
(856, 22, 25),  -- SEO Specialist (25%)

(857, 9, 100),  -- Senior Developer
(858, 14, 100), -- Data Analyst
(859, 28, 100), -- Accountant
(860, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(861, 33, 70),  -- IT Support Specialist (70%)
(861, 32, 30),  -- IT Support Manager (30%)

(862, 9, 100),  -- Senior Developer
(863, 10, 100), -- Junior Developer
(864, 16, 100), -- Senior Designer
(865, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(866, 18, 65),  -- Graphic Designer (65%)
(866, 19, 35),  -- UI/UX Designer (35%)

(867, 9, 100),  -- Senior Developer
(868, 31, 100), -- Sales Representative
(869, 28, 100), -- Accountant
(870, 10, 100), -- Junior Developer

-- Employee with multiple positions
(871, 11, 80),  -- QA Engineer (80%)
(871, 10, 20),  -- Junior Developer (20%)

(872, 9, 100),  -- Senior Developer
(873, 35, 100), -- Customer Support Specialist
(874, 21, 100), -- Content Creator
(875, 14, 100), -- Data Analyst

-- Employee with multiple positions
(876, 26, 75),  -- HR Assistant (75%)
(876, 25, 25),  -- Recruitment Specialist (25%)

(877, 9, 100),  -- Senior Developer
(878, 28, 100), -- Accountant
(879, 10, 100), -- Junior Developer
(880, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(881, 13, 70),  -- Data Scientist (70%)
(881, 15, 30),  -- Business Intelligence Analyst (30%)

(882, 9, 100),  -- Senior Developer
(883, 17, 100), -- Junior Designer
(884, 31, 100), -- Sales Representative
(885, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(886, 20, 60),  -- Digital Marketing Specialist (60%)
(886, 23, 40),  -- Social Media Manager (40%)

(887, 10, 100), -- Junior Developer
(888, 9, 100),  -- Senior Developer
(889, 28, 100), -- Accountant
(890, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(891, 33, 75),  -- IT Support Specialist (75%)
(891, 34, 25),  -- Network Administrator (25%)

(892, 9, 100),  -- Senior Developer
(893, 16, 100), -- Senior Designer
(894, 14, 100), -- Data Analyst
(895, 10, 100), -- Junior Developer

-- Employee with multiple positions
(896, 18, 80),  -- Graphic Designer (80%)
(896, 21, 20),  -- Content Creator (20%)

(897, 9, 100),  -- Senior Developer
(898, 31, 100), -- Sales Representative
(899, 28, 100), -- Accountant
(900, 35, 100), -- Customer Support Specialist
-- Employee with multiple positions
(901, 13, 60),  -- Data Scientist (60%)
(901, 14, 40),  -- Data Analyst (40%)

(902, 9, 100),  -- Senior Developer
(903, 10, 100), -- Junior Developer
(904, 28, 100), -- Accountant
(905, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(906, 20, 75),  -- Digital Marketing Specialist (75%)
(906, 22, 25),  -- SEO Specialist (25%)

(907, 9, 100),  -- Senior Developer
(908, 14, 100), -- Data Analyst
(909, 28, 100), -- Accountant
(910, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(911, 33, 70),  -- IT Support Specialist (70%)
(911, 32, 30),  -- IT Support Manager (30%)

(912, 9, 100),  -- Senior Developer
(913, 10, 100), -- Junior Developer
(914, 16, 100), -- Senior Designer
(915, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(916, 18, 65),  -- Graphic Designer (65%)
(916, 19, 35),  -- UI/UX Designer (35%)

(917, 9, 100),  -- Senior Developer
(918, 31, 100), -- Sales Representative
(919, 28, 100), -- Accountant
(920, 10, 100), -- Junior Developer

-- Employee with multiple positions
(921, 11, 80),  -- QA Engineer (80%)
(921, 10, 20),  -- Junior Developer (20%)

(922, 9, 100),  -- Senior Developer
(923, 35, 100), -- Customer Support Specialist
(924, 21, 100), -- Content Creator
(925, 14, 100), -- Data Analyst

-- Employee with multiple positions
(926, 26, 75),  -- HR Assistant (75%)
(926, 25, 25),  -- Recruitment Specialist (25%)

(927, 9, 100),  -- Senior Developer
(928, 28, 100), -- Accountant
(929, 10, 100), -- Junior Developer
(930, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(931, 13, 70),  -- Data Scientist (70%)
(931, 15, 30),  -- Business Intelligence Analyst (30%)

(932, 9, 100),  -- Senior Developer
(933, 17, 100), -- Junior Designer
(934, 31, 100), -- Sales Representative
(935, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(936, 20, 60),  -- Digital Marketing Specialist (60%)
(936, 23, 40),  -- Social Media Manager (40%)

(937, 10, 100), -- Junior Developer
(938, 9, 100),  -- Senior Developer
(939, 28, 100), -- Accountant
(940, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(941, 33, 75),  -- IT Support Specialist (75%)
(941, 34, 25),  -- Network Administrator (25%)

(942, 9, 100),  -- Senior Developer
(943, 16, 100), -- Senior Designer
(944, 14, 100), -- Data Analyst
(945, 10, 100), -- Junior Developer

-- Employee with multiple positions
(946, 18, 80),  -- Graphic Designer (80%)
(946, 21, 20),  -- Content Creator (20%)

(947, 9, 100),  -- Senior Developer
(948, 31, 100), -- Sales Representative
(949, 28, 100), -- Accountant
(950, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(951, 11, 65),  -- QA Engineer (65%)
(951, 9, 35),   -- Senior Developer (35%)

(952, 10, 100), -- Junior Developer
(953, 35, 100), -- Customer Support Specialist
(954, 21, 100), -- Content Creator
(955, 14, 100), -- Data Analyst

-- Employee with multiple positions
(956, 26, 70),  -- HR Assistant (70%)
(956, 24, 30),  -- HR Manager (30%)

(957, 9, 100),  -- Senior Developer
(958, 28, 100), -- Accountant
(959, 10, 100), -- Junior Developer
(960, 35, 100), -- Customer Support Specialist
-- Employee with multiple positions
(961, 13, 60),  -- Data Scientist (60%)
(961, 14, 40),  -- Data Analyst (40%)

(962, 9, 100),  -- Senior Developer
(963, 10, 100), -- Junior Developer
(964, 28, 100), -- Accountant
(965, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(966, 20, 75),  -- Digital Marketing Specialist (75%)
(966, 22, 25),  -- SEO Specialist (25%)

(967, 9, 100),  -- Senior Developer
(968, 14, 100), -- Data Analyst
(969, 28, 100), -- Accountant
(970, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(971, 33, 70),  -- IT Support Specialist (70%)
(971, 32, 30),  -- IT Support Manager (30%)

(972, 9, 100),  -- Senior Developer
(973, 10, 100), -- Junior Developer
(974, 16, 100), -- Senior Designer
(975, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(976, 18, 65),  -- Graphic Designer (65%)
(976, 19, 35),  -- UI/UX Designer (35%)

(977, 9, 100),  -- Senior Developer
(978, 31, 100), -- Sales Representative
(979, 28, 100), -- Accountant
(980, 10, 100), -- Junior Developer

-- Employee with multiple positions
(981, 11, 80),  -- QA Engineer (80%)
(981, 10, 20),  -- Junior Developer (20%)

(982, 9, 100),  -- Senior Developer
(983, 35, 100), -- Customer Support Specialist
(984, 21, 100), -- Content Creator
(985, 14, 100), -- Data Analyst

-- Employee with multiple positions
(986, 26, 75),  -- HR Assistant (75%)
(986, 25, 25),  -- Recruitment Specialist (25%)

(987, 9, 100),  -- Senior Developer
(988, 28, 100), -- Accountant
(989, 10, 100), -- Junior Developer
(990, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(991, 13, 70),  -- Data Scientist (70%)
(991, 15, 30),  -- Business Intelligence Analyst (30%)

(992, 9, 100),  -- Senior Developer
(993, 17, 100), -- Junior Designer
(994, 31, 100), -- Sales Representative
(995, 35, 100), -- Customer Support Specialist

-- Employee with multiple positions
(996, 20, 60),  -- Digital Marketing Specialist (60%)
(996, 23, 40),  -- Social Media Manager (40%)

(997, 10, 100), -- Junior Developer
(998, 9, 100),  -- Senior Developer
(999, 28, 100), -- Accountant
(1000, 35, 100), -- Customer Support Specialist
-- Employee with a single position
(1001, 9, 100),  -- Senior Developer
(1002, 10, 100), -- Junior Developer
(1003, 28, 100), -- Accountant
(1004, 35, 100), -- Customer Support Specialist
(1005, 14, 100), -- Data Analyst

-- Rare case: Employee with multiple positions
(1006, 20, 70),  -- Digital Marketing Specialist (70%)
(1006, 22, 30),  -- SEO Specialist (30%)

-- Employee with a single position
(1007, 9, 100),  -- Senior Developer
(1008, 31, 100), -- Sales Representative
(1009, 28, 100), -- Accountant
(1010, 10, 100), -- Junior Developer
(1011, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1012, 33, 80),  -- IT Support Specialist (80%)
(1012, 34, 20),  -- Network Administrator (20%)

-- Employee with a single position
(1013, 9, 100),  -- Senior Developer
(1014, 16, 100), -- Senior Designer
(1015, 14, 100), -- Data Analyst
(1016, 10, 100), -- Junior Developer
(1017, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1018, 18, 75),  -- Graphic Designer (75%)
(1018, 19, 25),  -- UI/UX Designer (25%)

-- Employee with a single position
(1019, 9, 100),  -- Senior Developer
(1020, 31, 100), -- Sales Representative
(1021, 28, 100), -- Accountant
(1022, 10, 100), -- Junior Developer
(1023, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1024, 11, 70),  -- QA Engineer (70%)
(1024, 10, 30),  -- Junior Developer (30%)

-- Employee with a single position
(1025, 9, 100),  -- Senior Developer
(1026, 35, 100), -- Customer Support Specialist
(1027, 21, 100), -- Content Creator
(1028, 14, 100), -- Data Analyst
(1029, 28, 100), -- Accountant

-- Rare case: Employee with multiple positions
(1030, 26, 65),  -- HR Assistant (65%)
(1030, 25, 35),  -- Recruitment Specialist (35%)

-- Employee with a single position
(1031, 9, 100),  -- Senior Developer
(1032, 10, 100), -- Junior Developer
(1033, 16, 100), -- Senior Designer
(1034, 35, 100), -- Customer Support Specialist
(1035, 14, 100), -- Data Analyst

-- Rare case: Employee with multiple positions
(1036, 13, 60),  -- Data Scientist (60%)
(1036, 15, 40),  -- Business Intelligence Analyst (40%)

-- Employee with a single position
(1037, 9, 100),  -- Senior Developer
(1038, 31, 100), -- Sales Representative
(1039, 28, 100), -- Accountant
(1040, 10, 100), -- Junior Developer
-- Employee with a single position
(1041, 9, 100),  -- Senior Developer
(1042, 10, 100), -- Junior Developer
(1043, 28, 100), -- Accountant
(1044, 35, 100), -- Customer Support Specialist
(1045, 14, 100), -- Data Analyst

-- Rare case: Employee with multiple positions
(1046, 20, 70),  -- Digital Marketing Specialist (70%)
(1046, 22, 30),  -- SEO Specialist (30%)

-- Employee with a single position
(1047, 9, 100),  -- Senior Developer
(1048, 31, 100), -- Sales Representative
(1049, 28, 100), -- Accountant
(1050, 10, 100), -- Junior Developer
(1051, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1052, 33, 80),  -- IT Support Specialist (80%)
(1052, 34, 20),  -- Network Administrator (20%)

-- Employee with a single position
(1053, 9, 100),  -- Senior Developer
(1054, 16, 100), -- Senior Designer
(1055, 14, 100), -- Data Analyst
(1056, 10, 100), -- Junior Developer
(1057, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1058, 18, 75),  -- Graphic Designer (75%)
(1058, 19, 25),  -- UI/UX Designer (25%)

-- Employee with a single position
(1059, 9, 100),  -- Senior Developer
(1060, 31, 100), -- Sales Representative
(1061, 28, 100), -- Accountant
(1062, 10, 100), -- Junior Developer
(1063, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1064, 11, 70),  -- QA Engineer (70%)
(1064, 10, 30),  -- Junior Developer (30%)

-- Employee with a single position
(1065, 9, 100),  -- Senior Developer
(1066, 35, 100), -- Customer Support Specialist
(1067, 21, 100), -- Content Creator
(1068, 14, 100), -- Data Analyst
(1069, 28, 100), -- Accountant

-- Rare case: Employee with multiple positions
(1070, 26, 65),  -- HR Assistant (65%)
(1070, 25, 35),  -- Recruitment Specialist (35%)

-- Employee with a single position
(1071, 9, 100),  -- Senior Developer
(1072, 10, 100), -- Junior Developer
(1073, 16, 100), -- Senior Designer
(1074, 35, 100), -- Customer Support Specialist
(1075, 14, 100), -- Data Analyst

-- Rare case: Employee with multiple positions
(1076, 13, 60),  -- Data Scientist (60%)
(1076, 15, 40),  -- Business Intelligence Analyst (40%)

-- Employee with a single position
(1077, 9, 100),  -- Senior Developer
(1078, 31, 100), -- Sales Representative
(1079, 28, 100), -- Accountant
(1080, 10, 100), -- Junior Developer

-- Employee with a single position
(1081, 9, 100),  -- Senior Developer
(1082, 10, 100), -- Junior Developer
(1083, 28, 100), -- Accountant
(1084, 35, 100), -- Customer Support Specialist
(1085, 14, 100), -- Data Analyst

-- Rare case: Employee with multiple positions
(1086, 20, 70),  -- Digital Marketing Specialist (70%)
(1086, 22, 30),  -- SEO Specialist (30%)

-- Employee with a single position
(1087, 9, 100),  -- Senior Developer
(1088, 31, 100), -- Sales Representative
(1089, 28, 100), -- Accountant
(1090, 10, 100), -- Junior Developer
(1091, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1092, 33, 80),  -- IT Support Specialist (80%)
(1092, 34, 20),  -- Network Administrator (20%)

-- Employee with a single position
(1093, 9, 100),  -- Senior Developer
(1094, 16, 100), -- Senior Designer
(1095, 14, 100), -- Data Analyst
(1096, 10, 100), -- Junior Developer
(1097, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1098, 18, 75),  -- Graphic Designer (75%)
(1098, 19, 25),  -- UI/UX Designer (25%)

-- Employee with a single position
(1099, 9, 100),  -- Senior Developer
(1100, 31, 100), -- Sales Representative
(1101, 28, 100), -- Accountant
(1102, 10, 100), -- Junior Developer
(1103, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1104, 11, 70),  -- QA Engineer (70%)
(1104, 10, 30),  -- Junior Developer (30%)

-- Employee with a single position
(1105, 9, 100),  -- Senior Developer
(1106, 35, 100), -- Customer Support Specialist
(1107, 21, 100), -- Content Creator
(1108, 14, 100), -- Data Analyst
(1109, 28, 100), -- Accountant

-- Rare case: Employee with multiple positions
(1110, 26, 65),  -- HR Assistant (65%)
(1110, 25, 35),  -- Recruitment Specialist (35%)

-- Employee with a single position
(1111, 9, 100),  -- Senior Developer
(1112, 10, 100), -- Junior Developer
(1113, 16, 100), -- Senior Designer
(1114, 35, 100), -- Customer Support Specialist
(1115, 14, 100), -- Data Analyst

-- Rare case: Employee with multiple positions
(1116, 13, 60),  -- Data Scientist (60%)
(1116, 15, 40),  -- Business Intelligence Analyst (40%)

-- Employee with a single position
(1117, 9, 100),  -- Senior Developer
(1118, 31, 100), -- Sales Representative
(1119, 28, 100), -- Accountant
(1120, 10, 100), -- Junior Developer
(1121, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1122, 20, 60),  -- Digital Marketing Specialist (60%)
(1122, 23, 40),  -- Social Media Manager (40%)

-- Employee with a single position
(1123, 9, 100),  -- Senior Developer
(1124, 14, 100), -- Data Analyst
(1125, 28, 100), -- Accountant
(1126, 35, 100), -- Customer Support Specialist
(1127, 10, 100), -- Junior Developer

-- Rare case: Employee with multiple positions
(1128, 33, 75),  -- IT Support Specialist (75%)
(1128, 34, 25),  -- Network Administrator (25%)

-- Employee with a single position
(1129, 9, 100),  -- Senior Developer
(1130, 16, 100), -- Senior Designer
(1131, 14, 100), -- Data Analyst
(1132, 10, 100), -- Junior Developer
(1133, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1134, 18, 80),  -- Graphic Designer (80%)
(1134, 21, 20),  -- Content Creator (20%)

-- Employee with a single position
(1135, 9, 100),  -- Senior Developer
(1136, 31, 100), -- Sales Representative
(1137, 28, 100), -- Accountant
(1138, 10, 100), -- Junior Developer
(1139, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1140, 11, 65),  -- QA Engineer (65%)
(1140, 9, 35),   -- Senior Developer (35%)

-- Employee with a single position
(1141, 10, 100), -- Junior Developer
(1142, 35, 100), -- Customer Support Specialist
(1143, 21, 100), -- Content Creator
(1144, 14, 100), -- Data Analyst
(1145, 28, 100), -- Accountant

-- Rare case: Employee with multiple positions
(1146, 26, 70),  -- HR Assistant (70%)
(1146, 24, 30),  -- HR Manager (30%)

-- Employee with a single position
(1147, 9, 100),  -- Senior Developer
(1148, 28, 100), -- Accountant
(1149, 10, 100), -- Junior Developer
(1150, 35, 100), -- Customer Support Specialist
-- Employee with a single position
(1151, 9, 100),  -- Senior Developer
(1152, 10, 100), -- Junior Developer
(1153, 28, 100), -- Accountant
(1154, 35, 100), -- Customer Support Specialist
(1155, 14, 100), -- Data Analyst

-- Rare case: Employee with multiple positions
(1156, 20, 70),  -- Digital Marketing Specialist (70%)
(1156, 22, 30),  -- SEO Specialist (30%)

-- Employee with a single position
(1157, 9, 100),  -- Senior Developer
(1158, 31, 100), -- Sales Representative
(1159, 28, 100), -- Accountant
(1160, 10, 100), -- Junior Developer
(1161, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1162, 33, 80),  -- IT Support Specialist (80%)
(1162, 34, 20),  -- Network Administrator (20%)

-- Employee with a single position
(1163, 9, 100),  -- Senior Developer
(1164, 16, 100), -- Senior Designer
(1165, 14, 100), -- Data Analyst
(1166, 10, 100), -- Junior Developer
(1167, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1168, 18, 75),  -- Graphic Designer (75%)
(1168, 19, 25),  -- UI/UX Designer (25%)

-- Employee with a single position
(1169, 9, 100),  -- Senior Developer
(1170, 31, 100), -- Sales Representative
(1171, 28, 100), -- Accountant
(1172, 10, 100), -- Junior Developer
(1173, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1174, 11, 70),  -- QA Engineer (70%)
(1174, 10, 30),  -- Junior Developer (30%)

-- Employee with a single position
(1175, 9, 100),  -- Senior Developer
(1176, 35, 100), -- Customer Support Specialist
(1177, 21, 100), -- Content Creator
(1178, 14, 100), -- Data Analyst
(1179, 28, 100), -- Accountant

-- Rare case: Employee with multiple positions
(1180, 26, 65),  -- HR Assistant (65%)
(1180, 25, 35),  -- Recruitment Specialist (35%)

-- Employee with a single position
(1181, 9, 100),  -- Senior Developer
(1182, 10, 100), -- Junior Developer
(1183, 16, 100), -- Senior Designer
(1184, 35, 100), -- Customer Support Specialist
(1185, 14, 100), -- Data Analyst

-- Rare case: Employee with multiple positions
(1186, 13, 60),  -- Data Scientist (60%)
(1186, 15, 40),  -- Business Intelligence Analyst (40%)

-- Employee with a single position
(1187, 9, 100),  -- Senior Developer
(1188, 31, 100), -- Sales Representative
(1189, 28, 100), -- Accountant
(1190, 10, 100), -- Junior Developer
(1191, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1192, 20, 60),  -- Digital Marketing Specialist (60%)
(1192, 23, 40),  -- Social Media Manager (40%)

-- Employee with a single position
(1193, 9, 100),  -- Senior Developer
(1194, 14, 100), -- Data Analyst
(1195, 28, 100), -- Accountant
(1196, 35, 100), -- Customer Support Specialist
(1197, 10, 100), -- Junior Developer

-- Rare case: Employee with multiple positions
(1198, 33, 75),  -- IT Support Specialist (75%)
(1198, 34, 25),  -- Network Administrator (25%)

-- Employee with a single position
(1199, 9, 100),  -- Senior Developer
(1200, 16, 100), -- Senior Designer
(1201, 14, 100), -- Data Analyst
(1202, 10, 100), -- Junior Developer
(1203, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1204, 18, 80),  -- Graphic Designer (80%)
(1204, 21, 20),  -- Content Creator (20%)

-- Employee with a single position
(1205, 9, 100),  -- Senior Developer
(1206, 31, 100), -- Sales Representative
(1207, 28, 100), -- Accountant
(1208, 10, 100), -- Junior Developer
(1209, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1210, 11, 65),  -- QA Engineer (65%)
(1210, 9, 35),   -- Senior Developer (35%)

-- Employee with a single position
(1211, 10, 100), -- Junior Developer
(1212, 35, 100), -- Customer Support Specialist
(1213, 21, 100), -- Content Creator
(1214, 14, 100), -- Data Analyst
(1215, 28, 100), -- Accountant

-- Rare case: Employee with multiple positions
(1216, 26, 70),  -- HR Assistant (70%)
(1216, 24, 30),  -- HR Manager (30%)

-- Employee with a single position
(1217, 9, 100),  -- Senior Developer
(1218, 28, 100), -- Accountant
(1219, 10, 100), -- Junior Developer
(1220, 35, 100), -- Customer Support Specialist

-- Employee with a single position
(1221, 9, 100),  -- Senior Developer
(1222, 10, 100), -- Junior Developer
(1223, 28, 100), -- Accountant
(1224, 35, 100), -- Customer Support Specialist
(1225, 14, 100), -- Data Analyst

-- Rare case: Employee with multiple positions
(1226, 20, 70),  -- Digital Marketing Specialist (70%)
(1226, 22, 30),  -- SEO Specialist (30%)

-- Employee with a single position
(1227, 9, 100),  -- Senior Developer
(1228, 31, 100), -- Sales Representative
(1229, 28, 100), -- Accountant
(1230, 10, 100), -- Junior Developer
(1231, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1232, 33, 80),  -- IT Support Specialist (80%)
(1232, 34, 20),  -- Network Administrator (20%)

-- Employee with a single position
(1233, 9, 100),  -- Senior Developer
(1234, 16, 100), -- Senior Designer
(1235, 14, 100), -- Data Analyst
(1236, 10, 100), -- Junior Developer
(1237, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1238, 18, 75),  -- Graphic Designer (75%)
(1238, 19, 25),  -- UI/UX Designer (25%)

-- Employee with a single position
(1239, 9, 100),  -- Senior Developer
(1240, 31, 100), -- Sales Representative
(1241, 28, 100), -- Accountant
(1242, 10, 100), -- Junior Developer
(1243, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1244, 11, 70),  -- QA Engineer (70%)
(1244, 10, 30),  -- Junior Developer (30%)

-- Employee with a single position
(1245, 9, 100),  -- Senior Developer
(1246, 35, 100), -- Customer Support Specialist
(1247, 21, 100), -- Content Creator
(1248, 14, 100), -- Data Analyst
(1249, 28, 100), -- Accountant

-- Rare case: Employee with multiple positions
(1250, 26, 65),  -- HR Assistant (65%)
(1250, 25, 35),  -- Recruitment Specialist (35%)

-- Employee with a single position
(1251, 9, 100),  -- Senior Developer
(1252, 10, 100), -- Junior Developer
(1253, 16, 100), -- Senior Designer
(1254, 35, 100), -- Customer Support Specialist
(1255, 14, 100), -- Data Analyst

-- Rare case: Employee with multiple positions
(1256, 13, 60),  -- Data Scientist (60%)
(1256, 15, 40),  -- Business Intelligence Analyst (40%)

-- Employee with a single position
(1257, 9, 100),  -- Senior Developer
(1258, 31, 100), -- Sales Representative
(1259, 28, 100), -- Accountant
(1260, 10, 100), -- Junior Developer
(1261, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1262, 20, 60),  -- Digital Marketing Specialist (60%)
(1262, 23, 40),  -- Social Media Manager (40%)

-- Employee with a single position
(1263, 9, 100),  -- Senior Developer
(1264, 14, 100), -- Data Analyst
(1265, 28, 100), -- Accountant
(1266, 35, 100), -- Customer Support Specialist
(1267, 10, 100), -- Junior Developer

-- Rare case: Employee with multiple positions
(1268, 33, 75),  -- IT Support Specialist (75%)
(1268, 34, 25),  -- Network Administrator (25%)

-- Employee with a single position
(1269, 9, 100),  -- Senior Developer
(1270, 16, 100), -- Senior Designer
(1271, 14, 100), -- Data Analyst
(1272, 10, 100), -- Junior Developer
(1273, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1274, 18, 80),  -- Graphic Designer (80%)
(1274, 21, 20),  -- Content Creator (20%)

-- Employee with a single position
(1275, 9, 100),  -- Senior Developer
(1276, 31, 100), -- Sales Representative
(1277, 28, 100), -- Accountant
(1278, 10, 100), -- Junior Developer
(1279, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1280, 11, 65),  -- QA Engineer (65%)
(1280, 9, 35),   -- Senior Developer (35%)

-- Employee with a single position
(1281, 10, 100), -- Junior Developer
(1282, 35, 100), -- Customer Support Specialist
(1283, 21, 100), -- Content Creator
(1284, 14, 100), -- Data Analyst
(1285, 28, 100), -- Accountant

-- Rare case: Employee with multiple positions
(1286, 26, 70),  -- HR Assistant (70%)
(1286, 24, 30),  -- HR Manager (30%)

-- Employee with a single position
(1287, 9, 100),  -- Senior Developer
(1288, 28, 100), -- Accountant
(1289, 10, 100), -- Junior Developer
(1290, 35, 100), -- Customer Support Specialist
-- Employee with a single position
(1291, 9, 100),  -- Senior Developer
(1292, 10, 100), -- Junior Developer
(1293, 28, 100), -- Accountant
(1294, 35, 100), -- Customer Support Specialist
(1295, 14, 100), -- Data Analyst

-- Rare case: Employee with multiple positions
(1296, 20, 70),  -- Digital Marketing Specialist (70%)
(1296, 22, 30),  -- SEO Specialist (30%)

-- Employee with a single position
(1297, 9, 100),  -- Senior Developer
(1298, 31, 100), -- Sales Representative
(1299, 28, 100), -- Accountant
(1300, 10, 100), -- Junior Developer
(1301, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1302, 33, 80),  -- IT Support Specialist (80%)
(1302, 34, 20),  -- Network Administrator (20%)

-- Employee with a single position
(1303, 9, 100),  -- Senior Developer
(1304, 16, 100), -- Senior Designer
(1305, 14, 100), -- Data Analyst
(1306, 10, 100), -- Junior Developer
(1307, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1308, 18, 75),  -- Graphic Designer (75%)
(1308, 19, 25),  -- UI/UX Designer (25%)

-- Employee with a single position
(1309, 9, 100),  -- Senior Developer
(1310, 31, 100), -- Sales Representative
(1311, 28, 100), -- Accountant
(1312, 10, 100), -- Junior Developer
(1313, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1314, 11, 70),  -- QA Engineer (70%)
(1314, 10, 30),  -- Junior Developer (30%)

-- Employee with a single position
(1315, 9, 100),  -- Senior Developer
(1316, 35, 100), -- Customer Support Specialist
(1317, 21, 100), -- Content Creator
(1318, 14, 100), -- Data Analyst
(1319, 28, 100), -- Accountant

-- Rare case: Employee with multiple positions
(1320, 26, 65),  -- HR Assistant (65%)
(1320, 25, 35),  -- Recruitment Specialist (35%)

-- Employee with a single position
(1321, 9, 100),  -- Senior Developer
(1322, 10, 100), -- Junior Developer
(1323, 16, 100), -- Senior Designer
(1324, 35, 100), -- Customer Support Specialist
(1325, 14, 100), -- Data Analyst

-- Rare case: Employee with multiple positions
(1326, 13, 60),  -- Data Scientist (60%)
(1326, 15, 40),  -- Business Intelligence Analyst (40%)

-- Employee with a single position
(1327, 9, 100),  -- Senior Developer
(1328, 31, 100), -- Sales Representative
(1329, 28, 100), -- Accountant
(1330, 10, 100), -- Junior Developer
(1331, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1332, 20, 60),  -- Digital Marketing Specialist (60%)
(1332, 23, 40),  -- Social Media Manager (40%)

-- Employee with a single position
(1333, 9, 100),  -- Senior Developer
(1334, 14, 100), -- Data Analyst
(1335, 28, 100), -- Accountant
(1336, 35, 100), -- Customer Support Specialist
(1337, 10, 100), -- Junior Developer

-- Rare case: Employee with multiple positions
(1338, 33, 75),  -- IT Support Specialist (75%)
(1338, 34, 25),  -- Network Administrator (25%)

-- Employee with a single position
(1339, 9, 100),  -- Senior Developer
(1340, 16, 100), -- Senior Designer
(1341, 14, 100), -- Data Analyst
(1342, 10, 100), -- Junior Developer
(1343, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1344, 18, 80),  -- Graphic Designer (80%)
(1344, 21, 20),  -- Content Creator (20%)

-- Employee with a single position
(1345, 9, 100),  -- Senior Developer
(1346, 31, 100), -- Sales Representative
(1347, 28, 100), -- Accountant
(1348, 10, 100), -- Junior Developer
(1349, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1350, 11, 65),  -- QA Engineer (65%)
(1350, 9, 35),   -- Senior Developer (35%)

-- Employee with a single position
(1351, 10, 100), -- Junior Developer
(1352, 35, 100), -- Customer Support Specialist
(1353, 21, 100), -- Content Creator
(1354, 14, 100), -- Data Analyst
(1355, 28, 100), -- Accountant

-- Rare case: Employee with multiple positions
(1356, 26, 70),  -- HR Assistant (70%)
(1356, 24, 30),  -- HR Manager (30%)

-- Employee with a single position
(1357, 9, 100),  -- Senior Developer
(1358, 28, 100), -- Accountant
(1359, 10, 100), -- Junior Developer
(1360, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1361, 13, 60),  -- Data Scientist (60%)
(1361, 14, 40),  -- Data Analyst (40%)

-- Employee with a single position
(1362, 9, 100),  -- Senior Developer
(1363, 10, 100), -- Junior Developer
(1364, 28, 100), -- Accountant
(1365, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1366, 20, 75),  -- Digital Marketing Specialist (75%)
(1366, 22, 25),  -- SEO Specialist (25%)

-- Employee with a single position
(1367, 9, 100),  -- Senior Developer
(1368, 14, 100), -- Data Analyst
(1369, 28, 100), -- Accountant
(1370, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1371, 33, 70),  -- IT Support Specialist (70%)
(1371, 32, 30),  -- IT Support Manager (30%)

-- Employee with a single position
(1372, 9, 100),  -- Senior Developer
(1373, 10, 100), -- Junior Developer
(1374, 16, 100), -- Senior Designer
(1375, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1376, 18, 65),  -- Graphic Designer (65%)
(1376, 19, 35),  -- UI/UX Designer (35%)

-- Employee with a single position
(1377, 9, 100),  -- Senior Developer
(1378, 31, 100), -- Sales Representative
(1379, 28, 100), -- Accountant
(1380, 10, 100), -- Junior Developer

-- Rare case: Employee with multiple positions
(1381, 11, 80),  -- QA Engineer (80%)
(1381, 10, 20),  -- Junior Developer (20%)

-- Employee with a single position
(1382, 9, 100),  -- Senior Developer
(1383, 35, 100), -- Customer Support Specialist
(1384, 21, 100), -- Content Creator
(1385, 14, 100), -- Data Analyst

-- Rare case: Employee with multiple positions
(1386, 26, 75),  -- HR Assistant (75%)
(1386, 25, 25),  -- Recruitment Specialist (25%)

-- Employee with a single position
(1387, 9, 100),  -- Senior Developer
(1388, 28, 100), -- Accountant
(1389, 10, 100), -- Junior Developer
(1390, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1391, 13, 70),  -- Data Scientist (70%)
(1391, 15, 30),  -- Business Intelligence Analyst (30%)

-- Employee with a single position
(1392, 9, 100),  -- Senior Developer
(1393, 17, 100), -- Junior Designer
(1394, 31, 100), -- Sales Representative
(1395, 35, 100), -- Customer Support Specialist

-- Rare case: Employee with multiple positions
(1396, 20, 60),  -- Digital Marketing Specialist (60%)
(1396, 23, 40),  -- Social Media Manager (40%)

-- Employee with a single position
(1397, 10, 100), -- Junior Developer
(1398, 9, 100),  -- Senior Developer
(1399, 28, 100), -- Accountant
(1400, 35, 100); -- Customer Support Specialist










UPDATE employees e
SET salary = COALESCE((SELECT SUM(p.salary * r.percentage / 100)
FROM emp_pos_relation r
JOIN positions p ON r.fk_position = p.id_position
WHERE r.fk_employee = e.id_employee), 0);

-- no fucking problema
