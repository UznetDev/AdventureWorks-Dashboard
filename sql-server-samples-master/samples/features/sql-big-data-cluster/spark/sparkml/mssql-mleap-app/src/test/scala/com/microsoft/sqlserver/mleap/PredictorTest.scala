package com.microsoft.sqlserver.mleap

import java.sql.Types

import org.scalatest.fixture

class PredictorTest extends fixture.FlatSpec {

  case class FixtureParam(input: PrimitiveDataset, scorer: Predictor, output: PrimitiveDataset)

  def withFixture(test: OneArgTest) = {
    val input: PrimitiveDataset = new PrimitiveDataset
    val scorer = new Predictor
    val output: PrimitiveDataset = new PrimitiveDataset
    val theFixture = FixtureParam(input, scorer, output)

    try {
      var columnId = 0
      input.addColumnMetadata(columnId, "age", java.sql.Types.INTEGER, 0, 0)
      input.addIntColumn(columnId, Array[Int](39, 50, 38), null)

      columnId += 1
      input.addColumnMetadata(columnId, "hours_per_week", java.sql.Types.INTEGER, 0, 0)
      input.addIntColumn(columnId, Array[Int](40, 13, 40), null)

      columnId += 1
      input.addColumnMetadata(columnId, "education", Types.NVARCHAR, 0, 0)
      input.addStringColumn(columnId, Array[String]("Bachelors", "Bachelors", "HS-grad"))

      columnId += 1
      input.addColumnMetadata(columnId, "sex", Types.NVARCHAR, 0, 0)
      input.addStringColumn(columnId, Array[String]("Male", "Male", "Male"))

      columnId += 1
      input.addColumnMetadata(columnId, "income", Types.NVARCHAR, 0, 0)
      input.addStringColumn(columnId, Array[String]("<=50K", "<=50K", "<=50K"))

      scorer.primitiveDataset2leapFrame(input)
      scorer.frame_out = scorer.frame_in
      scorer.leapFrame2primitiveDataset(output)

      withFixture(test.toNoArgTest(theFixture)) // "loan" the fixture to the test
    }
    finally () // clean up the fixture, nothing in this case
  }

  "A Predictor" should "be able to convert PrimitiveDataset to DefaultLeapFrame with same field names" in { f =>

    val columnNames = f.input.getColumnNames()
    val fieldNames = f.scorer.frame_in.schema.fields.map(_.name).toArray
    assert(fieldNames.deep == columnNames.deep)
  }

  it should "be able to convert DefaultLeapFrame to PrimitiveDataset with same column names" in { f =>

    val columnNames = f.output.getColumnNames()
    val fieldNames = f.scorer.frame_out.schema.fields.map(_.name).toArray
    assert(fieldNames.deep == columnNames.deep)
  }

  it should "be able to convert PrimitiveDataset to DefaultLeapFrame with same int field values" in { f =>

    val columnName = "age"
    val columnIndex = f.input.getColumnIndex(columnName)
    val columnValues = f.input.getIntColumn(columnIndex)

    val fieldNames = f.scorer.frame_in.schema.fields.map(_.name).toArray
    val iField = fieldNames.indexOf(columnName)
    val fieldValues = f.scorer.frame_in.dataset.map(_.getInt(iField)).toArray

    assert(fieldValues.deep == columnValues.deep)
  }

  it should "be able to convert DefaultLeapFrame to PrimitiveDataset with same int column values" in { f =>

    val columnName = "age"
    val columnIndex = f.input.getColumnIndex(columnName)
    val columnValues = f.input.getIntColumn(columnIndex)

    val fieldNames = f.scorer.frame_out.schema.fields.map(_.name).toArray
    val iField = fieldNames.indexOf(columnName)
    val fieldValues = f.scorer.frame_out.dataset.map(_.getInt(iField)).toArray

    assert(fieldValues.deep == columnValues.deep)
  }

  it should "be able to convert PrimitiveDataset to DefaultLeapFrame with same string field values" in { f =>

    val columnName = "education"
    val columnIndex = f.input.getColumnIndex(columnName)
    val columnValues = f.input.getStringColumn(columnIndex)

    val fieldNames = f.scorer.frame_in.schema.fields.map(_.name).toArray
    val iField = fieldNames.indexOf(columnName)
    val fieldValues = f.scorer.frame_in.dataset.map(_.getString(iField)).toArray

    assert(fieldValues.deep == columnValues.deep)
  }

  it should "be able to convert DefaultLeapFrame to PrimitiveDataset with same string column values" in { f =>

    val columnName = "education"
    val columnIndex = f.input.getColumnIndex(columnName)
    val columnValues = f.input.getStringColumn(columnIndex)

    val fieldNames = f.scorer.frame_out.schema.fields.map(_.name).toArray
    val iField = fieldNames.indexOf(columnName)
    val fieldValues = f.scorer.frame_out.dataset.map(_.getString(iField)).toArray

    assert(fieldValues.deep == columnValues.deep)
  }
}
