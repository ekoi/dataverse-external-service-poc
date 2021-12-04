# dataverse-external-service-poc


    CREATE OR REPLACE FUNCTION update_datasetversion_notify()
    RETURNS trigger AS
    $BODY$
    
    BEGIN
    PERFORM pg_notify('new_status', NEW.versionstate::text);
    RETURN NEW;
    END;
    $BODY$
    LANGUAGE plpgsql VOLATILE
    COST 100;
    ALTER FUNCTION update_datasetversion_notify()
    OWNER TO dvnuser;
    
    CREATE TRIGGER add_task_event_trigger
    AFTER UPDATE
    ON datasetversion
    FOR EACH ROW
    EXECUTE PROCEDURE update_datasetversion_notify();
