#!/usr/bin/env python3

# from https://stackoverflow.com/a/41294035/232485


def repeating_pattern(s: str) -> str | None:
    idx = -1
    j = 0
    for j in range(int(len(s) / 2)):
        idx = (s[j:] + s[j:]).find(s[j:], 1, -1)
        if idx != -1:
            # Make sure that the first substring is part of pattern
            if s[:j] == s[j:][:idx][-j:]:
                break
            #
        #
    #
    return None if idx == -1 else s[j:][:idx]


def main():
    # text = "geeksforgeeksforgeeksforgeeksforgeeksforgeeksforgeeksforgeeksforgeeksforgeeks"
    text = "6210045662100456621004566210045662100456621"

    print(repeating_pattern(text))


##############################################################################

if __name__ == "__main__":
    main()
