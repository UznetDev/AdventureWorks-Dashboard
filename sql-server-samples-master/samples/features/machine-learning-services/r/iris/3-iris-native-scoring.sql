Use sqlr;
GO

create or alter procedure native_predict_iris_species
as
begin
		declare @native_model varbinary(max) = (select native_model from iris_models where model_name = 'iris.dtree');
		-- Predict using native scoring on the specified model:
		/*Generate predictions using PREDICT function */

select p.*, d.Species as "Species.Actual", d.id
  from PREDICT(MODEL = @native_model, DATA = dbo.iris_data as d)
  with(setosa_Pred float, versicolor_Pred float, virginica_Pred float) as p;

end;
go

EXECUTE native_predict_iris_species;




