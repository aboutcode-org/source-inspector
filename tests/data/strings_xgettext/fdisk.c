/* vi: set sw=4 ts=4: */
/*
 * fdisk.c -- Partition table manipulator for Linux.
 *
 * Copyright (C) 1992  A. V. Le Blanc (LeBlanc@mcc.ac.uk)
 * Copyright (C) 2001,2002 Vladimir Oleynik <dzo@simtreas.ru> (initial bb port)
 *
 * Licensed under GPLv2 or later, see file LICENSE in this source tree.
 */
//applet:IF_FDISK(APPLET(fdisk, BB_DIR_SBIN, BB_SUID_DROP))

//kbuild:lib-$(CONFIG_FDISK) += fdisk.o

/* Looks like someone forgot to add this to config system */
//usage:#ifndef ENABLE_FEATURE_FDISK_BLKSIZE
#include "libbb.h"
#include "unicode.h"

static void list_types(const char *const *sys);
	"\x0a" "OS/2 Boot Manager",/* OS/2 Boot Manager */
	"\x42" "SFS",
	"\x63" "GNU HURD or SysV", /* GNU HURD or Mach or Sys V/386 (such as ISC UNIX) */
	"\x80" "Old Minix",        /* Minix 1.4a and earlier */
	"\x81" "Minix / old Linux",/* Minix 1.4b and later */
	"\x82" "Linux swap",       /* also Solaris */
	"\x83" "Linux",
	"\x84" "OS/2 hidden C: drive",
	"\x85" "Linux extended",
	"\x86" "NTFS volume set",
	"\x87" "NTFS volume set",
	"\x8e" "Linux LVM",
	"\x9f" "BSD/OS",           /* BSDI */
