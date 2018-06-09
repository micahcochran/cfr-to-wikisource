# cfr-to-wikisource

## Description
Script that scrape the XML of the U.S. Code of Federal Regulations (CFR) Title 3:
President Documents (Title 3).  This is a summary of presidential actions that happend in
the prior year, so the 2007 edition has documents from 2006.

The XML for the Code of Federal Regulation goes back to 1996, but Title
3 only starts in 2001.

**Note any examples are illustration, and may not look exactly the same in Wikimedia software**

## Requirements
Python 3.x  (likely 3.4+)

Install all the other requirements for these scripts by doing this:

```
 $ pip install -r requirements
```

## License
MIT   
see [LICENSE](LICENSE)



### proc-to-wikisource-list.py

Converts  Proclamation Table from Title 3 reformats it into wikitext for Wikisource's
lists of United States Presidential Proclamations.  There are 3 different
styles that it supports. Wikitext examples are in the source.

#### Example output for print_as_single_line()

*[Proclamation 9388](https://en.wikisource.org/wiki/Proclamation_9388) − To Take Certain Actions Under the African Growth and Opportunity Act (Jan. 11)
*[Proclamation 9389](https://en.wikisource.org/wiki/Proclamation_9389) − Religious Freedom Day, 2016 (Jan. 15)
*[Proclamation 9390](https://en.wikisource.org/wiki/Proclamation_9390) − Martin Luther King, Jr., Federal Holiday, 2016 (Jan. 15)
*[Proclamation 9391](https://en.wikisource.org/wiki/Proclamation_9391) − American Heart Month, 2016 (Jan. 29)

**Wikitext**
```MediaWiki
*[[Proclamation 9388]] − To Take Certain Actions Under the African Growth and Opportunity Act (Jan. 11)
*[[Proclamation 9389]] − Religious Freedom Day, 2016 (Jan. 15)
*[[Proclamation 9390]] − Martin Luther King, Jr., Federal Holiday, 2016 (Jan. 15)
*[[Proclamation 9391]] − American Heart Month, 2016 (Jan. 29)
```

#### Example output for print_as_wiki_table()

| No.                                                      | Signature Date |  Subject                                                             | 81 FR Page |
| -------------------------------------------------------- | -------------- | -------------------------------------------------------------------- | ---------- |
| [9388](https://en.wikisource.org/wiki/Proclamation_9388) | Jan. 11        | To Take Certain Actions Under the African Growth and Opportunity Act | 1851       |
| [9389](https://en.wikisource.org/wiki/Proclamation_9389) | Jan. 15        | Religious Freedom Day, 2016                                          | 3689       |


**Wikitext**
```MediaWiki
{|
! No.
! Signature Date
! Subject
! 81 FR Page
|-
|-
| [[Proclamation 9388|9388]]
| Jan. 11
| To Take Certain Actions Under the African Growth and Opportunity Act
| 1851
|-
| [[Proclamation 9389|9389]]
| Jan. 15
| Religious Freedom Day, 2016
| 3689
|-
```


#### Example output for print_as_wiki_hybrid_table() (Default)

| No.                                                                   |     | Subject                                                              | Signature Date | 81 FR Page |
| --------------------------------------------------------------------- |:---:| -------------------------------------------------------------------- | --------------:| ----------:|
| [Proclamation 9388](https://en.wikisource.org/wiki/Proclamation_9388) | −   | To Take Certain Actions Under the African Growth and Opportunity Act | Jan. 11        | 1851       |
| [Proclamation 9389](https://en.wikisource.org/wiki/Proclamation_9389) | −   | Religious Freedom Day, 2016                                          | Jan. 15        | 3689       |

**Wikitext**
```MediaWiki
{| style="valign:top;"
! Proc.&nbsp;No.
! &nbsp;
! align="left" | Subject
! <small>Signature Date</small>
! align="right" |&nbsp;&nbsp;<small>81 FR Page</small>
|-
| •&nbsp;[[Proclamation&nbsp;9388]]
| align="center" | −
| To Take Certain Actions Under the African Growth and Opportunity Act
| align="right" | Jan. 11
| align="right" | 1851
|-
| •&nbsp;[[Proclamation&nbsp;9389]]
| align="center" | −
| Religious Freedom Day, 2016
| align="right" | Jan. 15
| align="right" | 3689
|-
```
