import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

import org.apache.commons.logging.LogFactory;
import org.apache.commons.math3.stat.descriptive.DescriptiveStatistics;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

public class Bi_Stat {
  public final static Log LOGGER = LogFactory.getLog(Bi_Stat.class);

  public static class IMCMapper extends Mapper<Object, Text, Text, DoubleWritable> {

    private final Text effectif_text = new Text();
    private final Text ca_total_FL_text = new Text();
    private final Text ca_export_FK_text = new Text();
    private final Text risque_text = new Text();
    private final Text ratio_benef_text = new Text();

    private final Text evo_benefice_text = new Text();
    private final Text evo_effectif_text = new Text();

    private final Text evo_risque_text = new Text();
    private final Text age_text = new Text();


    Boolean is_first_row = true;

    public void map(Object key, Text value, Context context)
        throws IOException, InterruptedException {
      if (is_first_row) {
        is_first_row = false;
        return;
      }
      String[] row = value.toString().toLowerCase().split(",");

      if (!row[2].equals("NA") && !row[3].equals("NA") && !row[4].equals("NA") && !row[4].equals("na")
          && !row[5].equals("na") && !row[10].equals("na")) {
        DoubleWritable effectif = new DoubleWritable(Double.parseDouble(row[2]));
        DoubleWritable ca_total_FL = new DoubleWritable(Double.parseDouble(row[3]));
        DoubleWritable ca_export_FK = new DoubleWritable(Double.parseDouble(row[4]));
        String risque_ = row[5];
        String[] risque_val = risque_.toLowerCase().split("-");
        DoubleWritable risque = new DoubleWritable(0);
        if (risque_val.length == 2) {
          risque.set((Double.parseDouble(risque_val[0]) + Double.parseDouble(risque_val[1])) / 2);
        } else {
          risque.set(Double.parseDouble(risque_val[0]));
        }

        DoubleWritable evo_benefice = new DoubleWritable(Double.parseDouble(row[7]));
        DoubleWritable ratio_benef = new DoubleWritable(Double.parseDouble(row[8]));
        DoubleWritable evo_effectif = new DoubleWritable(Double.parseDouble(row[9]));

        DoubleWritable evo_risque = new DoubleWritable(Double.parseDouble(row[10]));
        DoubleWritable age = new DoubleWritable(Double.parseDouble(row[11]));

        effectif_text.set("effectif");
        ca_total_FL_text.set("ca_total_FL_text");
        ca_export_FK_text.set("ca_export_FK");
        risque_text.set("Risque");
        evo_benefice_text.set("evo_benefice");
        ratio_benef_text.set("ratio_benef");
        evo_effectif_text.set("evo_effectif");
        evo_risque_text.set("evo_risque");
        age_text.set("age");

        context.write(evo_effectif_text, evo_effectif);
        context.write(age_text, age);
        context.write(evo_risque_text, evo_risque);
        context.write(ratio_benef_text, ratio_benef);
        context.write(evo_benefice_text, evo_benefice);
        context.write(risque_text, risque);
        context.write(ca_export_FK_text, ca_export_FK);
        context.write(ca_total_FL_text, ca_total_FL);
        context.write(effectif_text, effectif);

      }else{
        LOGGER.info("ca_total_FL: "+row[3]);
        LOGGER.info("risque: "+row[5]);
        LOGGER.info("ca_export_FK: "+row[4]);
      }

    }
  }

  public static class IMCReducer extends Reducer<Text, DoubleWritable, Text, Text> {

    private final Text result = new Text();

    public void reduce(Text key, Iterable<DoubleWritable> values, Context context)
        throws IOException, InterruptedException {

      DescriptiveStatistics stats = new DescriptiveStatistics();

      for (DoubleWritable value : values) {
        stats.addValue(value.get());

        // Compute some statistics

      }

      double mean = stats.getMean();
      double min = stats.getMin();
      double max = stats.getMax();
      double std = stats.getStandardDeviation();
      double median = stats.getPercentile(50);
      double Q1 = stats.getPercentile(25);
      double Q3 = stats.getPercentile(75);
      

      String output = String.format(
          "=> Average: %.2f, Std: %.2f, Median: %.2f, Q1: %.2f, Q3: %.2f, Min: %.2f, Max: %.2f",
          mean, std, median, Q1, Q3, min, max);

      result.set(output);
      context.write(key, result);
    }
  }

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    conf.setLong("mapreduce.input.fileinputformat.split.maxsize", 134217728);

    Job job = Job.getInstance(conf, "Bi_Stat");
    job.setJarByClass(Bi_Stat.class);
    job.setMapperClass(IMCMapper.class);
    job.setReducerClass(IMCReducer.class);

    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(DoubleWritable.class);

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
