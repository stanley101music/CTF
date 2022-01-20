#include <iostream>
#include <fstream>
#include <string>
using namespace std;

const char* fl = "\x36\x44\x20\x28\x30\x24\x27\x01\x03\x3a\x0b\x0a\x06\x46\x1c\x11\x31\x1b\x08\x08\x07\x26\x36\x08\x1b\x17\x2d\x0d\x1c\x09\x01\x1c\x01\x14";

class entry
{
public:
	entry();
	~entry();
	void encrypt();
	void populate_key(char *a);
	void populate_member(char* a);
	bool compare(const char *a);
private:
	char member[34];
	char k[17];
};

entry::entry()
{
}

entry::~entry()
{
}

void entry::encrypt()
{
	for (int i = 0; i < 34; i++)
	{
		member[i] ^= k[i % 16];
	}
}

void entry::populate_key(char *a)
{
	strcpy_s(k, sizeof(k), a);
}

void entry::populate_member(char* a)
{
	memcpy(member, a, sizeof(member));
}

bool entry::compare(const char* a)
{
	bool chk = 1;
	for (int i = 0; i < 34; i++)
	{
		if (a[i] != member[i])
		{
			chk = 0;
			break;
		}
	}
	return chk;
}

int main()
{
	char a[40];
	entry* b = new entry;

	cout << "Are you ready for [REDACTED]?" << endl;
	cin.getline(a, 40);
	if (strcmp(a, "nimic_interesant"))
	{
		cout << "1000 pushups";
		return -1;
	}
	b->populate_key(a);

	ifstream f("nothing", ifstream::binary);
	if (!f)
	{
		cout << "50 burpees";
	}
	memset(a, 0, 40);
	f.read(a, 34);

	b->populate_member(a);
	b->encrypt();

	if (b->compare(fl))
	{
		cout << "Nice. Now go get your presents :D";
	}
	else
	{
		cout << "Just a few more crunches";
	}
}