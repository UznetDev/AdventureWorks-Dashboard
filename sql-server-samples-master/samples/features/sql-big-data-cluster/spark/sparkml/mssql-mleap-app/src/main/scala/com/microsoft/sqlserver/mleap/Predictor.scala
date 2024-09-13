package com.microsoft.sqlserver.mleap

import java.io.File
import java.util.logging.Logger
import java.util.logging.Level

import ml.combust.bundle.BundleFile
import ml.combust.mleap.runtime.MleapSupport._
import ml.combust.mleap.runtime.frame.Transformer
import resource._

class Predictor extends Score {
  var model: Transformer = null
  private val LOGGER = Logger.getLogger(classOf[Scorer].getName)

  def init(model_path: String) {
    LOGGER.info(s"init($model_path)")

    model = (for(bf <- managed(BundleFile(new File(model_path)))) yield {
      bf.loadMleapBundle()
    }).tried.flatMap(identity).get.root

    if (LOGGER.getLevel.intValue() <= Level.INFO.intValue()) {
      println("\nmodel schema fields:")
      model.schema.fields.zipWithIndex.foreach {
        case (field, idx) => println(s"$idx $field")
      }

      println("\nmodel inputSchema fields:")
      model.inputSchema.fields.zipWithIndex.foreach {
        case (field, idx) => println(s"$idx $field")
      }

      println("\nmodel outputSchema fields:")
      model.outputSchema.fields.zipWithIndex.foreach {
        case (field, idx) => println(s"$idx $field")
      }
    }

    LOGGER.info(s"model loaded...\n")
  }

  def run(): Unit = {
    frame_out = model.transform(frame_in).get

    if (LOGGER.getLevel.intValue() <= Level.INFO.intValue()) {
      println("\noutput schema fields:")
      frame_out.schema.fields.zipWithIndex.foreach {
        case (field, idx) => println(s"$idx $field")
      }
    }

    //leapFrame2json(frame_out)
  }

  def select(fieldNames: Array[String]) {
    if (fieldNames.nonEmpty && fieldNames.length != 1 && fieldNames(0) != "") {
      val allFieldNames = frame_out.schema.fields.map(_.name)
      if (!fieldNames.forall(allFieldNames.contains)) {
        throw new IllegalArgumentException(s"${fieldNames.toList} must be a subset of $allFieldNames")
      }

      frame_out = frame_out.select(fieldNames: _*).get
    }
  }
}
