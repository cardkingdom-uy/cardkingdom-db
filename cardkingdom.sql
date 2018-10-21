SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cardkingdom`
--

-- --------------------------------------------------------

--
-- Table structure for table `cards_coloridentity`
--

CREATE TABLE `cards_coloridentity` (
  `identity` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `uuid` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cards_colors`
--

CREATE TABLE `cards_colors` (
  `color` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `uuid` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cards_foreigndata`
--

CREATE TABLE `cards_foreigndata` (
  `foreigndata` int(10) NOT NULL,
  `uuid` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `language` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `flavorText` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `multiverseId` int(10) NOT NULL,
  `name` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `text` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cards_legalities`
--

CREATE TABLE `cards_legalities` (
  `format` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `uuid` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `legality` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cards_names`
--

CREATE TABLE `cards_names` (
  `nameId` int(10) NOT NULL,
  `uuid` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cards_prices`
--

CREATE TABLE `cards_prices` (
  `source` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `uuid` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `nm_price` decimal(15,8) NOT NULL,
  `ex_price` decimal(15,8) NOT NULL,
  `vg_price` decimal(15,8) NOT NULL,
  `g_price` decimal(15,8) NOT NULL,
  `url` text COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cards_printings`
--

CREATE TABLE `cards_printings` (
  `printing` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `uuid` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cards_rulings`
--

CREATE TABLE `cards_rulings` (
  `ruling` int(10) NOT NULL,
  `uuid` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` date NOT NULL,
  `text` text COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cards_subtypes`
--

CREATE TABLE `cards_subtypes` (
  `subtype` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `uuid` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cards_supertypes`
--

CREATE TABLE `cards_supertypes` (
  `supertype` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `uuid` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cards_types`
--

CREATE TABLE `cards_types` (
  `type` varchar(160) CHARACTER SET latin1 NOT NULL,
  `uuid` varchar(160) CHARACTER SET latin1 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sets`
--

CREATE TABLE `sets` (
  `setId` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `block` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `isOnlineOnly` tinyint(1) NOT NULL,
  `mtgoCode` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `releaseDate` date NOT NULL,
  `type` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sets_cards`
--

CREATE TABLE `sets_cards` (
  `setId` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `uuid` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `artist` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `borderColor` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `convertedManaCost` decimal(10,2) NOT NULL,
  `frameVersion` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `isFoilOnly` tinyint(1) NOT NULL,
  `hasFoil` tinyint(1) NOT NULL,
  `hasNonFoil` tinyint(1) NOT NULL,
  `isOnlineOnly` tinyint(1) NOT NULL,
  `isOversized` tinyint(1) NOT NULL,
  `isReserved` tinyint(1) NOT NULL,
  `layout` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `loyalty` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `manaCost` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `multiverseId` int(10) NOT NULL,
  `name` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `number` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `originalText` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `originalType` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `power` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rarity` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `text` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `toughness` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `flavorText` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `watermark` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sets_equiv`
--

CREATE TABLE `sets_equiv` (
  `setId` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `source` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `equiv` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sets_tokens`
--

CREATE TABLE `sets_tokens` (
  `setId` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `uuid` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `artist` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `borderColor` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `loyalty` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `number` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `power` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `text` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `toughness` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `watermark` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tokens_coloridentity`
--

CREATE TABLE `tokens_coloridentity` (
  `identity` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `uuid` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tokens_colors`
--

CREATE TABLE `tokens_colors` (
  `color` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `uuid` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tokens_reverserelated`
--

CREATE TABLE `tokens_reverserelated` (
  `reverseId` int(10) NOT NULL,
  `uuid` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cards_coloridentity`
--
ALTER TABLE `cards_coloridentity`
  ADD PRIMARY KEY (`identity`,`uuid`),
  ADD KEY `identity` (`identity`),
  ADD KEY `uuid` (`uuid`);

--
-- Indexes for table `cards_colors`
--
ALTER TABLE `cards_colors`
  ADD PRIMARY KEY (`color`,`uuid`),
  ADD KEY `color` (`color`),
  ADD KEY `uuid` (`uuid`);

--
-- Indexes for table `cards_foreigndata`
--
ALTER TABLE `cards_foreigndata`
  ADD PRIMARY KEY (`foreigndata`,`uuid`),
  ADD KEY `foreigndata` (`foreigndata`),
  ADD KEY `uuid` (`uuid`);

--
-- Indexes for table `cards_legalities`
--
ALTER TABLE `cards_legalities`
  ADD PRIMARY KEY (`format`,`uuid`),
  ADD KEY `format` (`format`),
  ADD KEY `uuid` (`uuid`);

--
-- Indexes for table `cards_names`
--
ALTER TABLE `cards_names`
  ADD PRIMARY KEY (`nameId`,`uuid`),
  ADD KEY `nameId` (`nameId`),
  ADD KEY `uuid` (`uuid`),
  ADD KEY `name` (`name`);

--
-- Indexes for table `cards_prices`
--
ALTER TABLE `cards_prices`
  ADD PRIMARY KEY (`source`,`uuid`,`date`),
  ADD KEY `source` (`source`),
  ADD KEY `uuid` (`uuid`),
  ADD KEY `date` (`date`),
  ADD KEY `uuid_2` (`uuid`,`date`),
  ADD KEY `source_2` (`source`,`uuid`,`date`);

--
-- Indexes for table `cards_printings`
--
ALTER TABLE `cards_printings`
  ADD PRIMARY KEY (`printing`,`uuid`),
  ADD KEY `printing` (`printing`),
  ADD KEY `uuid` (`uuid`);

--
-- Indexes for table `cards_rulings`
--
ALTER TABLE `cards_rulings`
  ADD PRIMARY KEY (`ruling`,`uuid`),
  ADD KEY `ruling` (`ruling`),
  ADD KEY `uuid` (`uuid`);

--
-- Indexes for table `cards_subtypes`
--
ALTER TABLE `cards_subtypes`
  ADD PRIMARY KEY (`subtype`,`uuid`),
  ADD KEY `subtype` (`subtype`),
  ADD KEY `uuid` (`uuid`);

--
-- Indexes for table `cards_supertypes`
--
ALTER TABLE `cards_supertypes`
  ADD PRIMARY KEY (`supertype`,`uuid`),
  ADD KEY `supertype` (`supertype`),
  ADD KEY `uuid` (`uuid`);

--
-- Indexes for table `cards_types`
--
ALTER TABLE `cards_types`
  ADD PRIMARY KEY (`type`,`uuid`),
  ADD KEY `type` (`type`),
  ADD KEY `uuid` (`uuid`);

--
-- Indexes for table `sets`
--
ALTER TABLE `sets`
  ADD PRIMARY KEY (`setId`),
  ADD KEY `setId` (`setId`),
  ADD KEY `name` (`name`);

--
-- Indexes for table `sets_cards`
--
ALTER TABLE `sets_cards`
  ADD PRIMARY KEY (`setId`,`uuid`),
  ADD KEY `setId` (`setId`),
  ADD KEY `uuid` (`uuid`),
  ADD KEY `name` (`name`),
  ADD KEY `type` (`type`),
  ADD KEY `multiverseId` (`multiverseId`);

--
-- Indexes for table `sets_equiv`
--
ALTER TABLE `sets_equiv`
  ADD PRIMARY KEY (`setId`,`source`),
  ADD KEY `setId` (`setId`),
  ADD KEY `source` (`source`);

--
-- Indexes for table `sets_tokens`
--
ALTER TABLE `sets_tokens`
  ADD PRIMARY KEY (`setId`,`uuid`),
  ADD KEY `setId` (`setId`),
  ADD KEY `uuid` (`uuid`),
  ADD KEY `name` (`name`);

--
-- Indexes for table `tokens_coloridentity`
--
ALTER TABLE `tokens_coloridentity`
  ADD PRIMARY KEY (`identity`,`uuid`),
  ADD KEY `identity` (`identity`),
  ADD KEY `uuid` (`uuid`);

--
-- Indexes for table `tokens_colors`
--
ALTER TABLE `tokens_colors`
  ADD PRIMARY KEY (`color`,`uuid`),
  ADD KEY `color` (`color`),
  ADD KEY `uuid` (`uuid`);

--
-- Indexes for table `tokens_reverserelated`
--
ALTER TABLE `tokens_reverserelated`
  ADD PRIMARY KEY (`reverseId`,`uuid`),
  ADD KEY `reverseId` (`reverseId`),
  ADD KEY `uuid` (`uuid`),
  ADD KEY `name` (`name`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;