#include <iostream>
#include <fstream>
using namespace std;


int main(int argc, char** argv)
{
    if(argc != 4)
    {
        cout << "Must insert as terminal parameters the name of the file, the multiplication factor and the name of the output file\n";
        return -1;
    }

    //Open file
    string in_file_name(argv[1]);
    ifstream in_file;
    in_file.open(in_file_name);
    if(!in_file.is_open())
    {
        cout << "Couldn't open the input file\n";
        return -1;
    }

    //Open a new file that will contain the new values
    string out_file_name(argv[3]);
    ofstream out_file;
    out_file.open(out_file_name);
    if(!out_file.is_open())
    {
        cout << "Couldn't create the output file\n";
        return -1;
    }

    string line, substring, newline;
    double value;
    int start_index, line_element;

    //Don't change the first line
    getline(in_file, line);
    out_file << line << "\n";

    //Read each line
    while(getline(in_file, line))
    {
        //Reset params
        newline = "";
        start_index = 0;
        line_element = 0;

        //Analyze the line
        for(int i = 0; i < line.length(); i++)
        {
            //Don't change the id
            if(line[i] == ',' && line_element == 0)
            {
                line_element++;
                substring = line.substr(start_index, i - start_index);
                newline += substring + ",";
                start_index = i+1;
            }
            else if(line[i] == ',' && ( i - start_index ) > 0 )
            {
                substring = line.substr(start_index, i - start_index);
                try
                {
                    value = stod(substring);
                }
                catch(...)
                {
                    value = 0;
                }
                value *= atof(argv[2]);
                newline += to_string(value) + ",";
                start_index = i+1;
            }
            else if(line[i] == ',' && ( i - start_index ) == 0 )
            {
                //Insert a void space
                newline += ",";
                start_index++;
            }
        }
        //Last element of the line
        if( ( line.length() - 1 - start_index ) > 0 )
        {
            substring = line.substr(start_index, line.length() - start_index);
            try
            {
                value = stod(substring);
            }
            catch(...)
            {
                value = 0;
            }
            value *= atof(argv[2]);
            newline += to_string(value);
        }

        //Write the line in the new file
        out_file << newline << "\n";
    }

    //Close both files
    in_file.close();
    out_file.close();
    if(in_file.is_open() || out_file.is_open())
    {
        cout << "One of the file couldn't be closed\n";
        return -1;
    }

    //End
    return 0;
}