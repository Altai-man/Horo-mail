using System;
using System.Net;
using System.IO;
using System.Drawing;
using System.Windows.Forms;
using System.Text.RegularExpressions;
using System.Threading;
using System.Diagnostics;

public class WebParser {

  static public string Getting () {
    try {
      using (WebClient client = new WebClient ()) {
        Stream data = client.OpenRead ("http://www.horochan.ru");
        StreamReader reader = new StreamReader (data);
        string s = reader.ReadToEnd ();
        data.Close ();
        reader.Close ();
        return s;
      }
    }
    catch (Exception ex) {
      MessageBox.Show("Looks like Internet connection is off, set connection on or send log to autor.");
      System.IO.File.WriteAllText(@"error_log", ex.Message);
      return ""; // Fiction. Dirty.
    }
  }


  static public bool Check (string testing) {
    String line = "";
    if (System.IO.File.Exists("source")) {
      using (StreamReader sr = new StreamReader(@"source")) {
        line += sr.ReadToEnd();
      }
      System.IO.File.Delete(@"source"); // Deleting original file after reading.
      if (String.Compare(line, testing) == 0) {
        System.IO.File.WriteAllText(@"source", testing);
        return true; // True if strings are equal.
      }
      else {
        System.IO.File.WriteAllText(@"source", testing);
        return false;
      }
    }
    else {
      System.IO.File.WriteAllText(@"source", testing);
      return true;
    }
  }

  static public string[] Parser (string source) {
    //Initialize array of strings.
    string[] parsed = new string[10];

    //Splitting...
    string[] substrings = Regex.Split(source, "<!-- REPLY CONTAINER -->");

    string result = substrings[1];

    source = result.Replace("\"", "_"); // Replace HTML special characters.
    //Compile re-patterns.
    string post_num = @"[0-9][0-9][0-9][0-9][0-9]*";
    string board_name = @"/[abd]";
    string thread_num = @"/[0-9][0-9][0-9][0-9][0-9]*/";
    string text = @"(?s)<div class=_message_>.*?</div>";
    string pic_link = @"http://horochan.ru/data/thumb/thumb_.*?.(jpg|png|bmp)";


    //Return post number.
    Match post_match = Regex.Match(source, post_num);
    if (post_match.Success ) {
      parsed[0] = post_match.Value;
    }
    else {
      MessageBox.Show("Looks like \"Horochan\" is not working now. Please, contact Administrator or me with contacts, which you can find in readme file. Sorry for that.");
      Application.Exit();
    }


    //Return board name.
    Match board_match = Regex.Match(source, board_name);
    if (board_match.Success ) {
      parsed[1] = board_match.Value;
    }
    else {
      MessageBox.Show("Looks like \"Horochan\" is not working now. Please, contact Administrator or me with contacts, which you can find in readme file. Sorry for that.");
      Application.Exit();
    }


    //Return thread number.
    Match thread_match = Regex.Match(source, thread_num);
    if (thread_match.Success ) {
      parsed[2] = thread_match.Value;
    }
    else {
      MessageBox.Show("Looks like \"Horochan\" is not working now. Please, contact Administrator or me with contacts, which you can find in readme file. Sorry for that.");
      Application.Exit();
    }


    //Return text
    Match text_match = Regex.Match(source, text);
    if (text_match.Success ) {
      string tmp= text_match.Value.Replace(@"<div class=_message_>", "");
      parsed[3] = Regex.Replace(tmp, "<[^>]+?>", "");
      parsed[3] = parsed[3].Replace("&gt;", ">");
    }
    else {
      parsed[3] = "No text.";
    }


    //Return pic_link.
    Match pic_link_match = Regex.Match(source, pic_link);
    if (pic_link_match.Success ) {
      parsed[4] = pic_link_match.Value;
    }
    else {
      parsed[4] = "";
    }

    return parsed; // Return all array of parsed sources.
  }
}


public class Horo : Form {

  //Window.
  public Horo (string[] parsed) {
    // Window properties.
    this.Text = "Horo-mail";
    this.Size = new System.Drawing.Size(500, 200);
    this.FormBorderStyle = FormBorderStyle.None;
    this.MaximizeBox = false;
    this.Opacity = 0.85;
    this.BackColor = Color.Black;

    // Picture.
    if (System.IO.File.Exists("tmp_pic.jpg")) {
      System.IO.File.Delete(@"tmp_pic.jpg"); // Deleting original.
    }
    if (parsed[4].Length > 0) {
      WebClient webClient = new WebClient();
      webClient.DownloadFile(parsed[4], @"tmp_pic.jpg");
      Image image1 = new Bitmap(@"tmp_pic.jpg");
      PictureBox pictureBox1 = new PictureBox();
      pictureBox1.SizeMode = PictureBoxSizeMode.Zoom;
      pictureBox1.BorderStyle = BorderStyle.None;
      pictureBox1.ClientSize = new Size(150, 150);
      pictureBox1.Location = new Point(10, 10);
      pictureBox1.Image = (Image) image1;

      Controls.Add(pictureBox1);
    }

    else {
      Image image1 = new Bitmap(@"no_image.jpg");
      PictureBox pictureBox1 = new PictureBox();
      pictureBox1.SizeMode = PictureBoxSizeMode.Zoom;
      pictureBox1.BorderStyle = BorderStyle.None;
      pictureBox1.ClientSize = new Size(150, 150);
      pictureBox1.Location = new Point(10, 25);
      pictureBox1.Image = (Image) image1;

      Controls.Add(pictureBox1);
    }

    //Label.
    Label label1 = new Label();
    label1.BorderStyle = System.Windows.Forms.BorderStyle.None;
    label1.UseMnemonic = true; // I'm newbie with C#, sorry.

    label1.Location = new Point (170, 25);
    label1.ForeColor = System.Drawing.Color.White;
    string CheckedText = "Post №:" + parsed[0] + "\n";
    CheckedText += "From thread: " + parsed[1] + parsed[2] + "\n";
    if (parsed[3].Length == 0)
      {
        CheckedText += "No text.";
      }
    if (parsed[3].Length > 250) {
      parsed[3] = parsed[3].Remove(250);
      CheckedText += "Message: " + parsed[3] + "...\n";
    }
    else
      {
        CheckedText += parsed[3];
      }
    label1.Size = new Size (250, 160);
    label1.Text = CheckedText;

    Controls.Add (label1);

    //Button for exit.
    Button button1 = new Button ();
    button1.Click += new EventHandler (Button_Click);
    button1.Text = "Continue";
    button1.TextAlign = ContentAlignment.TopLeft;
    button1.Size = new Size(60, 21);
    button1.Location = new Point(430, 15);
    button1.ForeColor = System.Drawing.Color.White;

    Controls.Add (button1);

    //Button for kill.
    Button button2 = new Button ();
    button2.Click += new EventHandler (OnExit);
    button2.Text = "Kill";
    button2.TextAlign = ContentAlignment.TopLeft;
    button2.Size = new Size(50, 21);
    button2.Location = new Point(430, 50);
    button2.ForeColor = System.Drawing.Color.White;

    Controls.Add (button2);
  }

  // Killing func.
  private void OnExit(object sender, EventArgs e)
  {
    Process.GetCurrentProcess().CloseMainWindow();
  }

  // Click on button.
  private void Button_Click (object sender, EventArgs e)
  {
    Application.Exit(); // For user.
  }

  // Main.
  static public void Main () {
    while (true) {
      var source = WebParser.Getting();
      bool result = WebParser.Check(source);
      if (result == false) {
        if (source != "") {
          var parsed = WebParser.Parser(source);
          Application.Run (new Horo (parsed));
        }
        System.Threading.Thread.Sleep(15000);
      }
      else {
        System.Threading.Thread.Sleep(15000);
      }
    }
  }
}