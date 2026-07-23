import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { requireRole } from "@/lib/require-role";

export const dynamic = "force-dynamic";

export async function GET(_request: Request, { params }: { params: { id: string } }) {
  const { organization } = await requireRole(["OWNER", "COACH"]);

  const week = await prisma.week.findFirst({
    where: { id: params.id, organizationId: organization.id },
    include: { pdf: true },
  });

  if (!week?.pdf) {
    return new NextResponse(null, { status: 404 });
  }

  const filename = week.semana.replace(/[\r\n"]/g, "").trim() || "okami";

  return new NextResponse(week.pdf.data, {
    headers: {
      "Content-Type": week.pdf.mimeType,
      "Content-Disposition": `inline; filename="${filename}.pdf"`,
    },
  });
}
