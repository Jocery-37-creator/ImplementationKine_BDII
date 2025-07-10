-- ============================================
-- Trigger Function for pocket 
-- ============================================
CREATE OR REPLACE FUNCTION validate_pocket_goal_fields()
RETURNS TRIGGER AS $$
BEGIN
  -- Si es una meta de ahorro
  IF NEW.is_goal = TRUE THEN
    IF NEW.goal IS NULL OR NEW.regularity IS NULL OR NEW.quota IS NULL THEN
      RAISE EXCEPTION 'Campos goal, regularity y quota no pueden ser NULL cuando is_goal = TRUE';
    END IF;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- Trigger for pocket 
-- ============================================
CREATE TRIGGER trg_validate_pocket_goal
BEFORE INSERT OR UPDATE ON "Pocket"
FOR EACH ROW
EXECUTE FUNCTION validate_pocket_goal_fields();