SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS `metar` ;
CREATE SCHEMA IF NOT EXISTS `metar` DEFAULT CHARACTER SET utf8 ;
USE `metar` ;

-- -----------------------------------------------------
-- Table `metar`.`station`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `metar`.`station` ;

CREATE  TABLE IF NOT EXISTS `metar`.`station` (
  `idstation` INT NOT NULL ,
  `code` VARCHAR(4) NOT NULL ,
  `lat` VARCHAR(45) NULL ,
  `long` VARCHAR(45) NULL ,
  PRIMARY KEY (`idstation`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `metar`.`observation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `metar`.`observation` ;

CREATE  TABLE IF NOT EXISTS `metar`.`observation` (
  `idobservation` INT NOT NULL AUTO_INCREMENT ,
  `station_idstation` INT NOT NULL ,
  `code` VARCHAR(4) NOT NULL ,
  `time` DATETIME NOT NULL ,
  `temperature` MEDIUMINT NULL ,
  `wind_speed` DECIMAL(2,1) NULL ,
  `wind_direction` MEDIUMINT NULL ,
  PRIMARY KEY (`idobservation`) ,
  INDEX `fk_observation_station` (`station_idstation` ASC) ,
  UNIQUE INDEX `unique_observation` (`code` ASC, `time` ASC) ,
  CONSTRAINT `fk_observation_station`
    FOREIGN KEY (`station_idstation` )
    REFERENCES `metar`.`station` (`idstation` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
