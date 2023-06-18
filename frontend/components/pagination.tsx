import Link from "next/link";

type PaginationProps = {
  target: string;
  currentPage: number;
  totalPages: number;
  pages: number[];
};

const Pagination = ({
  target,
  currentPage,
  totalPages,
  pages,
}: PaginationProps) => (
  <div>
    <nav className="text-green-800 space-x-5">
      <Link
        href={`/${target}?page=${currentPage - 1}`}
        className={currentPage > 1 ? "" : "pointer-events-none"}
      >
        &lt;
      </Link>
      {pages.map((page: number) => (
        <Link
          key={page}
          href={`/${target}?page=${page}`}
          className={currentPage == page ? "pointer-events-none font-bold" : ""}
        >
          {page}
        </Link>
      ))}
      <Link
        href={`/${target}?page=${currentPage + 1}`}
        className={currentPage < totalPages ? "" : "pointer-events-none"}
      >
        &gt;
      </Link>
    </nav>
  </div>
);

export default Pagination;
