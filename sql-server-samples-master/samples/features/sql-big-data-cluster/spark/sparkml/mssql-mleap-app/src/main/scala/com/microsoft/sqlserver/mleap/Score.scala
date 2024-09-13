package com.microsoft.sqlserver.mleap

import java.io.File
import java.sql.{JDBCType, Types}

import ml.combust.mleap.runtime.MleapSupport._
import ml.combust.mleap.runtime.frame.{DefaultLeapFrame, Row}
import ml.combust.mleap.runtime.serialization.{BuiltinFormats, FrameReader}
import ml.combust.mleap.core.types._
import ml.combust.mleap.tensor.{ByteString, DenseTensor, SparseTensor}

trait Score {

  var frame_in: DefaultLeapFrame = null
  var frame_out: DefaultLeapFrame = null

  def getScalaType(sqlType: Int): ScalarType = {
    sqlType match {
      case Types.BIT => ScalarType.Boolean
      case Types.TINYINT => ScalarType.Byte
      case Types.SMALLINT => ScalarType.Short
      case Types.INTEGER => ScalarType.Int
      case Types.BIGINT => ScalarType.Long
      case Types.FLOAT => ScalarType.Float
      case Types.DOUBLE => ScalarType.Double
      case Types.NVARCHAR => ScalarType.String
      case Types.BINARY => ScalarType.ByteString
      case _ => throw new IllegalArgumentException("unsupported sql type: " + JDBCType.valueOf(sqlType).getName)
    }
  }

  def getSqlType(mleapType: BasicType): Int = {
    mleapType match {
      case BasicType.Boolean => Types.BIT
      case BasicType.Byte => Types.TINYINT
      case BasicType.Short => Types.SMALLINT
      case BasicType.Int => Types.INTEGER
      case BasicType.Long => Types.BIGINT
      case BasicType.Float => Types.FLOAT
      case BasicType.Double => Types.DOUBLE
      case BasicType.String => Types.NVARCHAR
      case BasicType.ByteString => Types.BINARY
      case _ => throw new IllegalArgumentException("unsupported mleap type: " + mleapType)
    }
  }

  def primitiveDataset2leapFrame(input: PrimitiveDataset) {
    val nCols = input.getColumnCount()
    val nRows = input.getRowCount(0) // assuming columns have the same length

    // Create a schema.
    val fields = List.newBuilder[StructField]
    for (iCol <- 0 until nCols) {
      fields += StructField(input.getColumnName(iCol), getScalaType(input.getColumnType(iCol)))
    }
    val schema = StructType(fields.result).get

    // Create a dataset to contain all of our values
    val seqBuilder = Seq.newBuilder[Row]
    for (iRow <- 0 until nRows) {
      val values = List.newBuilder[Any]
      for (iCol <- 0 until nCols) {
        val columnType = input.getColumnType(iCol)
        values += (columnType match {
          case Types.BIT => input.getBooleanColumn(iCol)(iRow)
          case Types.SMALLINT => input.getShortColumn(iCol)(iRow)
          case Types.INTEGER => input.getIntColumn(iCol)(iRow)
          case Types.BIGINT => input.getLongColumn(iCol)(iRow)
          case Types.FLOAT => input.getFloatColumn(iCol)(iRow)
          case Types.DOUBLE => input.getDoubleColumn(iCol)(iRow)
          case Types.NVARCHAR => input.getStringColumn(iCol)(iRow)
          case Types.VARBINARY => input.getBinaryColumn(iCol)(iRow)
          case Types.DATE => input.getDateColumn(iCol)(iRow)
          case _ => throw new IllegalArgumentException(s"No BasicType $columnType")
        })
      }
      seqBuilder += Row(values.result: _*)
    }

    val dataset = seqBuilder.result

    // Create a LeapFrame from the schema and dataset
    frame_in = DefaultLeapFrame(schema, dataset)
  }

  def leapFrame2primitiveDataset(output: PrimitiveDataset) {

    val nRows = frame_out.dataset.length
    var nCols = 0

    val schema = frame_out.schema
    val fields = schema.fields

    println("\nouput columns:")
    for (iField <- 0 until fields.length) {
      val field: StructField = fields(iField)
      val name = field.name
      val dataType = field.dataType
      val base = dataType.base
      val shape = dataType.shape

      if (shape.isTensor) {
        val nDims = shape.asInstanceOf[TensorShape].dimensions.get.length
        frame_out.dataset(0).getTensor(iField) match {
          case dense: DenseTensor[_] => {
            println(s"\t$name: DenseTensor[$base]")
          }
          case sparse: SparseTensor[_] => {
            println(s"\t$name: SparseTensor[$base]")
          }
        }

        for (iDim <- 0 until nDims) {
          val nSlots = field.dataType.shape.asInstanceOf[TensorShape].dimensions.get(iDim)

          for (iSlot <- 0 until nSlots) {
            output.addColumnMetadata(nCols, name + iSlot, getSqlType(base), 0, 0)
            base match {
              case BasicType.Boolean => {
                val outputDataCol = frame_out.dataset.map(_.getTensor[Boolean](iField).toDense.values(iSlot)).toArray
                output.addBooleanColumn(nCols, outputDataCol, null)
              }
              case BasicType.Byte => {
                val outputDataCol = frame_out.dataset.map(_.getTensor[Byte](iField).toDense.values(iSlot).toShort).toArray
                output.addShortColumn(nCols, outputDataCol, null)
              }
              case BasicType.Short => {
                val outputDataCol = frame_out.dataset.map(_.getTensor[Short](iField).toDense.values(iSlot)).toArray
                output.addShortColumn(nCols, outputDataCol, null)
              }
              case BasicType.Int => {
                val outputDataCol = frame_out.dataset.map(_.getTensor[Int](iField).toDense.values(iSlot)).toArray
                output.addIntColumn(nCols, outputDataCol, null)
              }
              case BasicType.Long => {
                val outputDataCol = frame_out.dataset.map(_.getTensor[Long](iField).toDense.values(iSlot)).toArray
                output.addLongColumn(nCols, outputDataCol, null)
              }
              case BasicType.Float => {
                val outputDataCol = frame_out.dataset.map(_.getTensor[Float](iField).toDense.values(iSlot)).toArray
                output.addFloatColumn(nCols, outputDataCol, null)
              }
              case BasicType.Double => {
                val outputDataCol = frame_out.dataset.map(_.getTensor[Double](iField).toDense.values(iSlot)).toArray
                output.addDoubleColumn(nCols, outputDataCol, null)
              }
              case BasicType.String => {
                val outputDataCol = frame_out.dataset.map(_.getTensor[String](iField).toDense.values(iSlot)).toArray
                output.addStringColumn(nCols, outputDataCol)
              }
              case BasicType.ByteString => {
                val outputDataCol = frame_out.dataset.map(_.getTensor[ByteString](iField).toDense.values(iSlot).bytes).toArray
                output.addBinaryColumn(nCols, outputDataCol)
              }
              case _ => throw new IllegalArgumentException(s"No BasicType $base")
            }

            nCols += 1
          }
        }
      } else {
        println(s"\t$name: ScalarType.$base")

        output.addColumnMetadata(nCols, name, getSqlType(base), 0, 0)
        base match {
          case BasicType.Boolean => {
            val outputDataCol = frame_out.dataset.map(_.getBool(iField)).toArray
            output.addBooleanColumn(nCols, outputDataCol, null)
          }
          case BasicType.Byte => {
            val outputDataCol = frame_out.dataset.map(_.getByte(iField).toShort).toArray
            output.addShortColumn(nCols, outputDataCol, null)
          }
          case BasicType.Short => {
            val outputDataCol = frame_out.dataset.map(_.getShort(iField)).toArray
            output.addShortColumn(nCols, outputDataCol, null)
          }
          case BasicType.Int => {
            val outputDataCol = frame_out.dataset.map(_.getInt(iField)).toArray
            output.addIntColumn(nCols, outputDataCol, null)
          }
          case BasicType.Long => {
            val outputDataCol = frame_out.dataset.map(_.getLong(iField)).toArray
            output.addLongColumn(nCols, outputDataCol, null)
          }
          case BasicType.Float => {
            val outputDataCol = frame_out.dataset.map(_.getFloat(iField)).toArray
            output.addFloatColumn(nCols, outputDataCol, null)
          }
          case BasicType.Double => {
            val outputDataCol = frame_out.dataset.map(_.getDouble(iField)).toArray
            output.addDoubleColumn(nCols, outputDataCol, null)
          }
          case BasicType.String => {
            val outputDataCol = frame_out.dataset.map(_.getString(iField)).toArray
            output.addStringColumn(nCols, outputDataCol)
          }
          case BasicType.ByteString => {
            val outputDataCol = frame_out.dataset.map(_.getByteString(iField).bytes).toArray
            output.addBinaryColumn(nCols, outputDataCol)
          }
          case _ => throw new IllegalArgumentException(s"No BasicType $base")
        }
        nCols += 1
      }
    }
  }

  def json2leapFrame(frame_path: String) {
    println (s"run($frame_path)")

    val f = new File (frame_path)
    if (f.exists () && ! f.isDirectory () ) {
      // get input from file
      frame_in = FrameReader (BuiltinFormats.json).read (f).get
    } else {
      // get input from string
      frame_in = FrameReader (BuiltinFormats.json).fromBytes (frame_path.getBytes () ).get
    }
  }

  def leapFrame2json(frame: DefaultLeapFrame): String = {
    var json_str: String = null
    for(bytes <- frame.writer("ml.combust.mleap.json").toBytes();
        frame2 <- FrameReader("ml.combust.mleap.json").fromBytes(bytes)) {
      json_str = new String(bytes)
      assert(frame == frame2)
    }

    println()
    println(json_str)

    return json_str
  }
}
